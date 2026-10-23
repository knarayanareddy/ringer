package com.roomsmith.puzzle

object PuzzleEngineTestSuite {
    private var passed = 0

    private val alignment = PuzzleRequirement(
        subject = "red_cup",
        predicate = "left_of",
        target = "book",
        minConfidence = 0.70,
        normalizedMargin = 0.05
    )
    private val openPalm = PuzzleRequirement("hand", "open_palm", minConfidence = 0.75)
    private val sequenceRequirements = listOf(
        PuzzleRequirement("blue_cup", "inside_zone", "zone_lens", 0.70, minimumOverlap = 0.60),
        PuzzleRequirement(
            "book",
            "inside_zone",
            "zone_archive",
            0.70,
            minimumOverlap = 0.60,
            maxIntervalAfterPreviousMs = 30_000
        )
    )

    private fun engine(noTiming: Boolean = false) = PuzzleEngine(
        sessionId = "fixture-session",
        calibrationVersion = "mat-v1",
        objectKitVersion = "kit-v1",
        noTimingMode = noTiming
    )

    private fun observation(
        puzzleId: String = "lighthouse_alignment",
        subject: String = "red_cup",
        predicate: String = "left_of",
        target: String? = "book",
        confidence: Double = 0.90,
        margin: Double? = 0.10,
        overlap: Double? = null,
        at: Long,
        sequence: Long,
        valid: Boolean = true,
        present: Boolean = true
    ) = Observation(
        puzzleId = puzzleId,
        sessionId = "fixture-session",
        calibrationVersion = "mat-v1",
        objectKitVersion = "kit-v1",
        subject = subject,
        predicate = predicate,
        target = target,
        confidence = confidence,
        normalizedMargin = margin,
        overlap = overlap,
        observedAtMs = at,
        sequence = sequence,
        calibrationValid = valid,
        candidatePresent = present
    )

    private fun expect(name: String, block: () -> Unit) {
        block()
        passed += 1
        println("PASS $name")
    }

    @JvmStatic
    fun main(args: Array<String>) {
        expect("short alignment hold does not complete") {
            val game = engine()
            check(game.submit(listOf(alignment), 1000, observation(at = 0, sequence = 1)).isEmpty())
            check(game.submit(listOf(alignment), 1000, observation(at = 500, sequence = 2)).isEmpty())
        }
        expect("stable alignment completes exactly once") {
            val game = engine()
            game.submit(listOf(alignment), 1000, observation(at = 0, sequence = 1))
            val events = game.submit(listOf(alignment), 1000, observation(at = 1000, sequence = 2))
            check(events.size == 1)
            check(game.submit(listOf(alignment), 1000, observation(at = 1100, sequence = 3)).isEmpty())
            check(game.caseReport().size == 1)
        }
        expect("wrong relation and low confidence never succeed") {
            val game = engine()
            check(game.submit(listOf(alignment), 0, observation(predicate = "right_of", at = 0, sequence = 1)).isEmpty())
            check(game.submit(listOf(alignment), 0, observation(confidence = 0.69, at = 0, sequence = 2)).isEmpty())
            check(game.submit(listOf(alignment), 0, observation(margin = 0.01, at = 0, sequence = 3)).isEmpty())
            check(game.submit(listOf(alignment), 0, observation(subject = "unknown_cup", at = 0, sequence = 4)).isEmpty())
        }
        expect("open palm requires confidence and hold") {
            val game = engine()
            check(game.submit(listOf(openPalm), 750, observation(puzzleId = "raise_the_shield", subject = "hand", predicate = "open_palm", target = null, confidence = 0.74, margin = null, at = 0, sequence = 1)).isEmpty())
            game.submit(listOf(openPalm), 750, observation(puzzleId = "raise_the_shield", subject = "hand", predicate = "open_palm", target = null, margin = null, at = 0, sequence = 2))
            check(game.submit(listOf(openPalm), 750, observation(puzzleId = "raise_the_shield", subject = "hand", predicate = "open_palm", target = null, margin = null, at = 500, sequence = 3)).isEmpty())
            check(game.submit(listOf(openPalm), 750, observation(puzzleId = "raise_the_shield", subject = "hand", predicate = "open_palm", target = null, margin = null, at = 750, sequence = 4)).size == 1)
        }
        expect("calibration loss cancels the active hold") {
            val game = engine()
            game.submit(listOf(alignment), 1000, observation(at = 0, sequence = 1))
            game.submit(listOf(alignment), 1000, observation(at = 500, sequence = 2, valid = false))
            game.submit(listOf(alignment), 1000, observation(at = 1500, sequence = 3))
            check(game.submit(listOf(alignment), 1000, observation(at = 2000, sequence = 4)).isEmpty())
            check(game.submit(listOf(alignment), 1000, observation(at = 2500, sequence = 5)).size == 1)
        }
        expect("one missing candidate is tolerated but not two") {
            val tolerant = engine()
            tolerant.submit(listOf(alignment), 1000, observation(at = 0, sequence = 1))
            tolerant.submit(listOf(alignment), 1000, observation(at = 500, sequence = 2, present = false))
            check(tolerant.submit(listOf(alignment), 1000, observation(at = 1000, sequence = 3)).size == 1)

            val reset = engine()
            reset.submit(listOf(alignment), 1000, observation(at = 0, sequence = 1))
            reset.submit(listOf(alignment), 1000, observation(at = 400, sequence = 2, present = false))
            reset.submit(listOf(alignment), 1000, observation(at = 500, sequence = 3, present = false))
            check(reset.submit(listOf(alignment), 1000, observation(at = 1000, sequence = 4)).isEmpty())
        }
        expect("stale observations cannot complete or replay") {
            val game = engine()
            game.submit(listOf(alignment), 1000, observation(at = 0, sequence = 1))
            check(game.submit(listOf(alignment), 1000, observation(at = 1000, sequence = 1)).isEmpty())
            check(game.submit(listOf(alignment), 1000, observation(at = 999, sequence = 0)).isEmpty())
            check(game.submit(listOf(alignment), 1000, observation(at = 1000, sequence = 2)).size == 1)
        }
        expect("wrong sequence order is rejected") {
            val game = engine()
            val wrong = observation(puzzleId = "lens_archive_sequence", subject = "book", predicate = "inside_zone", target = "zone_archive", margin = null, overlap = 0.8, at = 0, sequence = 1)
            check(game.submit(sequenceRequirements, 500, wrong).isEmpty())
            check(game.state.sequenceSteps["lens_archive_sequence"] == null)
        }
        expect("ordered stable sequence completes") {
            val game = engine()
            val lens = { at: Long, sequence: Long -> observation(puzzleId = "lens_archive_sequence", subject = "blue_cup", predicate = "inside_zone", target = "zone_lens", margin = null, overlap = 0.8, at = at, sequence = sequence) }
            val book = { at: Long, sequence: Long -> observation(puzzleId = "lens_archive_sequence", subject = "book", predicate = "inside_zone", target = "zone_archive", margin = null, overlap = 0.8, at = at, sequence = sequence) }
            game.submit(sequenceRequirements, 500, lens(0, 1))
            game.submit(sequenceRequirements, 500, lens(500, 2))
            game.submit(sequenceRequirements, 500, book(1000, 3))
            check(game.submit(sequenceRequirements, 500, book(1500, 4)).size == 1)
        }
        expect("sequence timeout resets standard mode") {
            val game = engine()
            val lens = { at: Long, sequence: Long -> observation(puzzleId = "lens_archive_sequence", subject = "blue_cup", predicate = "inside_zone", target = "zone_lens", margin = null, overlap = 0.8, at = at, sequence = sequence) }
            val book = { at: Long, sequence: Long -> observation(puzzleId = "lens_archive_sequence", subject = "book", predicate = "inside_zone", target = "zone_archive", margin = null, overlap = 0.8, at = at, sequence = sequence) }
            game.submit(sequenceRequirements, 500, lens(0, 1))
            game.submit(sequenceRequirements, 500, lens(500, 2))
            game.submit(sequenceRequirements, 500, book(31_000, 3))
            check(game.submit(sequenceRequirements, 500, book(31_500, 4)).isEmpty())
        }
        expect("no-timing preserves order without interval failure") {
            val game = engine(noTiming = true)
            val lens = { at: Long, sequence: Long -> observation(puzzleId = "lens_archive_sequence", subject = "blue_cup", predicate = "inside_zone", target = "zone_lens", margin = null, overlap = 0.8, at = at, sequence = sequence) }
            val book = { at: Long, sequence: Long -> observation(puzzleId = "lens_archive_sequence", subject = "book", predicate = "inside_zone", target = "zone_archive", margin = null, overlap = 0.8, at = at, sequence = sequence) }
            game.submit(sequenceRequirements, 500, lens(0, 1))
            game.submit(sequenceRequirements, 500, lens(500, 2))
            game.submit(sequenceRequirements, 500, book(31_000, 3))
            check(game.submit(sequenceRequirements, 500, book(31_500, 4)).size == 1)
        }
        expect("remote fallback uses authored answer and expected sequence") {
            val game = engine()
            check(game.commitRemote("lighthouse_alignment", listOf("option_red_left"), listOf("option_red_right"), 0).isEmpty())
            check(game.state.stateSequence == 0L)
            check(runCatching {
                game.commitRemote("lighthouse_alignment", listOf("option_red_left", "option_red_left"), listOf("option_red_left", "option_red_left"), 0)
            }.isFailure)
            check(game.commitRemote("lighthouse_alignment", listOf("option_red_left"), listOf("option_red_left"), 0).size == 1)
            check(game.commitRemote("lighthouse_alignment", listOf("option_red_left"), listOf("option_red_left"), 0).isEmpty())
        }
        expect("resumed completion does not replay and report has no media") {
            val completion = CompletedPuzzle("lighthouse_alignment", CompletionPath.REMOTE, 1)
            val resumed = PuzzleEngine("fixture-session", "mat-v1", "kit-v1", initialState = EngineState(1, mapOf(completion.puzzleId to completion)))
            check(resumed.commitRemote("lighthouse_alignment", listOf("option_red_left"), listOf("option_red_left"), 1).isEmpty())
            check(resumed.caseReport() == listOf(completion))
        }
        println("PASS $passed Kotlin puzzle-engine tests")
    }
}
