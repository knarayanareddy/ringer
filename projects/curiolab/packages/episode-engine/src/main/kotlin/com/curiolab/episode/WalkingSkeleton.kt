package com.curiolab.episode

object WalkingSkeleton {
    @JvmStatic
    fun main(args: Array<String>) {
        val initial = EpisodeState()
        val afterFlatPrediction = initial.commitPrediction(Trial.FLAT.predictionKey, "folded", 0)
        val afterFlat = afterFlatPrediction.confirmMeasurement(Trial.FLAT, 3, 1)
        val afterFoldedPrediction = afterFlat.commitPrediction(Trial.FOLDED.predictionKey, "more", 2)
        val completed = afterFoldedPrediction.confirmMeasurement(Trial.FOLDED, 7, 3)
        val summary = completed.measuredSummary()
        println(
            """
            {
              "mode": "FIXTURE ONLY — no Fire TV, companion, camera, relay, or AWS connection",
              "flat_load": ${summary.flatLoad},
              "folded_load": ${summary.foldedLoad},
              "comparison": "${summary.comparison.name.lowercase()}",
              "branch_node_id": "${summary.comparison.branchNodeId}",
              "state_sequence": ${completed.stateSequence},
              "notice": "Deterministic engine walk only; no physical experiment or learning outcome is claimed."
            }
            """.trimIndent()
        )
    }
}
