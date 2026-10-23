package com.roomsmith.puzzle

object WalkingSkeleton {
    @JvmStatic
    fun main(args: Array<String>) {
        val puzzles = listOf(
            RemotePuzzle(
                "lighthouse_alignment",
                RemoteInteraction.SINGLE_CHOICE,
                listOf("option_red_left")
            ),
            RemotePuzzle(
                "raise_the_shield",
                RemoteInteraction.HOLD,
                listOf("option_shield"),
                holdMs = 750,
                authoredHints = listOf("Use the large shield control; no camera is needed.")
            ),
            RemotePuzzle(
                "lens_archive_sequence",
                RemoteInteraction.ORDERED_ACTIONS,
                listOf("option_lens_then_archive")
            )
        )
        val session = RemoteEpisodeSession(
            sessionId = "fixture-session",
            episodeId = "fixture-lighthouse",
            contentVersion = "0.1.0",
            puzzles = puzzles
        )
        session.submitRemote("lighthouse_alignment", listOf("option_red_left"), 0, 0)
        session.authoredHint("raise_the_shield", 1, 1)

        val resumed = RemoteEpisodeSession(
            sessionId = "fixture-session",
            episodeId = "fixture-lighthouse",
            contentVersion = "0.1.0",
            puzzles = puzzles,
            initialSnapshot = session.snapshot
        )
        resumed.submitRemote("raise_the_shield", listOf("option_shield"), 1, 100)
        resumed.submitRemote("raise_the_shield", listOf("option_shield"), 1, 850)
        resumed.recordActiveTime(1200)
        resumed.submitRemote("lens_archive_sequence", listOf("option_lens_then_archive"), 2, 1000)
        val report = resumed.caseReport()
        println(
            """
            {
              "mode": "FIXTURE REMOTE PATH ONLY — no Fire TV, companion, camera, WebRTC, or AWS connection",
              "completed_puzzles": ${report.completedPuzzles.size},
              "completion_paths": [${report.completedPuzzles.joinToString(",") { "\"${it.puzzleId}:${it.path.name.lowercase()}\"" }}],
              "state_sequence": ${resumed.snapshot.engineState.stateSequence},
              "hints_used": ${report.hintsUsed.values.sum()},
              "elapsed_active_time_ms": ${report.elapsedActiveTimeMs},
              "snapshot_resume_exercised": true,
              "room_media_in_report": false,
              "notice": "In-memory ordered remote-state walk only; elapsed time is fixture input, and no durable restart, rendered offline app, or physical playtest is claimed."
            }
            """.trimIndent()
        )
    }
}
