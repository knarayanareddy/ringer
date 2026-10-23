package com.roomsmith.puzzle

enum class RemoteInteraction { SINGLE_CHOICE, HOLD, ORDERED_ACTIONS }

data class RemotePuzzle(
    val puzzleId: String,
    val interaction: RemoteInteraction,
    val correctOptionIds: List<String>,
    val holdMs: Long = 0,
    val authoredHints: List<String> = emptyList()
)

data class RemoteEpisodeSnapshot(
    val engineState: EngineState = EngineState(),
    val hintsUsed: Map<String, Int> = emptyMap(),
    val activeTimeMs: Long = 0
)

data class EpisodeCaseReport(
    val episodeId: String,
    val contentVersion: String,
    val completedPuzzles: List<CompletedPuzzle>,
    val hintsUsed: Map<String, Int>,
    val elapsedActiveTimeMs: Long
)

/** Ordered remote-only episode coordinator. Snapshots are values, not a durable store. */
class RemoteEpisodeSession(
    private val sessionId: String,
    private val episodeId: String,
    private val contentVersion: String,
    private val puzzles: List<RemotePuzzle>,
    private val noTimingMode: Boolean = false,
    initialSnapshot: RemoteEpisodeSnapshot = RemoteEpisodeSnapshot()
) {
    private val engine = PuzzleEngine(
        sessionId = sessionId,
        calibrationVersion = "remote-not-used",
        objectKitVersion = "remote-not-used",
        noTimingMode = noTimingMode,
        initialState = initialSnapshot.engineState
    )
    private val remoteHolds = mutableMapOf<String, Long>()
    private var hintsUsed = initialSnapshot.hintsUsed.toMap()
    private var activeTimeMs = initialSnapshot.activeTimeMs

    init {
        require(sessionId.isNotBlank() && episodeId.isNotBlank() && contentVersion.isNotBlank()) {
            "Session and episode identifiers are required"
        }
        require(puzzles.isNotEmpty()) { "At least one authored puzzle is required" }
        require(puzzles.map { it.puzzleId }.toSet().size == puzzles.size) { "Duplicate puzzle IDs" }
        puzzles.forEach { puzzle ->
            require(puzzle.correctOptionIds.isNotEmpty()) { "A remote solution is required" }
            require(puzzle.correctOptionIds.toSet().size == puzzle.correctOptionIds.size) {
                "Duplicate authored remote solutions are invalid"
            }
            require(puzzle.holdMs >= 0) { "Remote hold duration cannot be negative" }
            require(puzzle.authoredHints.all { it.isNotBlank() && it.split(Regex("\\s+")).size <= 45 }) {
                "Authored hints must be non-blank and at most 45 words"
            }
        }
        require(activeTimeMs >= 0) { "Active time cannot be negative" }
        require(hintsUsed.keys.all { key -> puzzles.any { it.puzzleId == key } }) {
            "Hint history references an unknown puzzle"
        }
        require(hintsUsed.values.all { it >= 0 }) { "Hint levels cannot be negative" }
        require(hintsUsed.all { (puzzleId, level) ->
            level <= puzzles.first { it.puzzleId == puzzleId }.authoredHints.size
        }) { "Hint history exceeds the authored ladder" }
        val puzzleIds = puzzles.map { it.puzzleId }
        require(engine.state.completedPuzzles.keys.all { it in puzzleIds }) {
            "Snapshot contains an unknown completed puzzle"
        }
        val completedOrder = engine.caseReport().map { it.puzzleId }
        require(completedOrder == puzzleIds.filter { it in engine.state.completedPuzzles }) {
            "Snapshot completions violate authored order"
        }
    }

    val snapshot: RemoteEpisodeSnapshot
        get() = RemoteEpisodeSnapshot(engine.state, hintsUsed, activeTimeMs)

    private fun currentPuzzle(): RemotePuzzle? = puzzles.firstOrNull {
        it.puzzleId !in engine.state.completedPuzzles
    }

    private fun requireCurrent(puzzleId: String): RemotePuzzle {
        val puzzle = puzzles.firstOrNull { it.puzzleId == puzzleId }
        requireNotNull(puzzle) { "Unknown authored puzzle" }
        require(currentPuzzle()?.puzzleId == puzzleId) { "Puzzle is not the current authored step" }
        return puzzle
    }

    fun submitRemote(
        puzzleId: String,
        selectedOptionIds: List<String>,
        expectedStateSequence: Long,
        atMs: Long
    ): List<PuzzleCompleted> {
        require(atMs >= 0) { "Remote action timestamp cannot be negative" }
        if (puzzleId in engine.state.completedPuzzles) return emptyList()
        val puzzle = requireCurrent(puzzleId)
        val correctSelection = if (puzzle.interaction == RemoteInteraction.ORDERED_ACTIONS) {
            selectedOptionIds == puzzle.correctOptionIds
        } else {
            selectedOptionIds.size == puzzle.correctOptionIds.size &&
                selectedOptionIds.toSet() == puzzle.correctOptionIds.toSet()
        }
        if (!correctSelection) {
            remoteHolds.remove(puzzleId)
            require(expectedStateSequence == engine.state.stateSequence) {
                "Stale remote fallback state sequence"
            }
            return emptyList()
        }
        if (puzzle.interaction == RemoteInteraction.HOLD && !noTimingMode) {
            val startedAt = remoteHolds[puzzleId]
            if (startedAt == null || atMs < startedAt || atMs - startedAt < puzzle.holdMs) {
                remoteHolds[puzzleId] = if (startedAt != null && atMs < startedAt) atMs else startedAt ?: atMs
                return emptyList()
            }
        }
        val events = engine.commitRemote(
            puzzleId,
            puzzle.correctOptionIds,
            selectedOptionIds,
            expectedStateSequence
        )
        if (events.isNotEmpty()) remoteHolds.remove(puzzleId)
        return events
    }

    fun authoredHint(puzzleId: String, level: Int, expectedStateSequence: Long): String {
        val puzzle = requireCurrent(puzzleId)
        require(expectedStateSequence == engine.state.stateSequence) { "Stale hint state sequence" }
        val priorLevel = hintsUsed[puzzleId] ?: 0
        require(level in 1..puzzle.authoredHints.size) { "Hint level is not authored" }
        require(level <= priorLevel + 1) { "Hint levels cannot be skipped" }
        if (level > priorLevel) hintsUsed = hintsUsed + (puzzleId to level)
        return puzzle.authoredHints[level - 1]
    }

    fun recordActiveTime(deltaMs: Long) {
        require(deltaMs >= 0) { "Active time delta cannot be negative" }
        activeTimeMs = Math.addExact(activeTimeMs, deltaMs)
    }

    fun caseReport(): EpisodeCaseReport {
        require(currentPuzzle() == null) { "Case report requires every authored puzzle" }
        return EpisodeCaseReport(
            episodeId = episodeId,
            contentVersion = contentVersion,
            completedPuzzles = engine.caseReport(),
            hintsUsed = hintsUsed,
            elapsedActiveTimeMs = activeTimeMs
        )
    }
}
