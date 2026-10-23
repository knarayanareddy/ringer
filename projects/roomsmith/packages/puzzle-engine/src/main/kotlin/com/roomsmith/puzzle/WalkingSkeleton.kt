package com.roomsmith.puzzle

object WalkingSkeleton {
    @JvmStatic
    fun main(args: Array<String>) {
        val engine = PuzzleEngine(
            sessionId = "fixture-session",
            calibrationVersion = "fixture-not-used",
            objectKitVersion = "fixture-not-used"
        )
        engine.commitRemote("lighthouse_alignment", listOf("option_red_left"), listOf("option_red_left"), 0)
        engine.commitRemote("raise_the_shield", listOf("option_shield"), listOf("option_shield"), 1)
        engine.commitRemote(
            "lens_archive_sequence",
            listOf("option_lens_then_archive"),
            listOf("option_lens_then_archive"),
            2
        )
        val report = engine.caseReport()
        println(
            """
            {
              "mode": "FIXTURE REMOTE PATH ONLY — no Fire TV, companion, camera, WebRTC, or AWS connection",
              "completed_puzzles": ${report.size},
              "completion_paths": [${report.joinToString(",") { "\"${it.puzzleId}:${it.path.name.lowercase()}\"" }}],
              "state_sequence": ${engine.state.stateSequence},
              "room_media_in_report": false,
              "notice": "Deterministic remote-state walk only; no rendered episode or physical playtest is claimed."
            }
            """.trimIndent()
        )
    }
}
