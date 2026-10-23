package com.curiolab.episode

object WalkingSkeleton {
    @JvmStatic
    fun main(args: Array<String>) {
        val session = ManualEpisodeSession()
        session.acknowledgeSafety(
            adultConsent = true,
            safetyInstructionsAccepted = true,
            smallObjectSupervisionConfirmed = true,
            expectedSequence = 0
        )
        session.commitPrediction(Trial.FLAT, "folded", 1)
        session.markStop(Trial.FLAT, 5, 2)
        session.confirmStoppedMeasurement(Trial.FLAT, 4, 3)

        val resumed = ManualEpisodeSession(session.snapshot)
        resumed.commitPrediction(Trial.FOLDED, "more", 4)
        resumed.markStop(Trial.FOLDED, 7, 5)
        resumed.confirmStoppedMeasurement(Trial.FOLDED, 7, 6)
        resumed.acknowledgeComparison(7)
        resumed.commitReflection("shape_can_matter", 8)
        val summary = resumed.measuredSummary()
        println(
            """
            {
              "mode": "FIXTURE MANUAL PATH ONLY — no Fire TV, companion, camera, relay, or AWS connection",
              "stage": "${resumed.snapshot.stage.name.lowercase()}",
              "camera_mode": "${resumed.snapshot.cameraMode}",
              "flat_stopped_count": ${resumed.snapshot.stoppedMeasurements.getValue(Trial.FLAT).lastStableCount},
              "flat_load": ${summary.flatLoad},
              "folded_load": ${summary.foldedLoad},
              "comparison": "${summary.comparison.name.lowercase()}",
              "branch_node_id": "${summary.branchNodeId}",
              "state_sequence": ${resumed.snapshot.sequence},
              "snapshot_resume_exercised": true,
              "notice": "In-memory deterministic manual walk only; no durable restart, physical experiment, rendered scene, or learning outcome is claimed."
            }
            """.trimIndent()
        )
    }
}
