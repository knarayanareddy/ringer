package com.curiolab.episode

object EpisodeEngineTestSuite {
    private var passed = 0

    private fun expect(name: String, block: () -> Unit) {
        block()
        passed += 1
        println("PASS $name")
    }

    private fun stateWithBothPredictions(): EpisodeState = EpisodeState()
        .commitPrediction(Trial.FLAT.predictionKey, "unsure", 0)
        .commitPrediction(Trial.FOLDED.predictionKey, "unsure", 1)

    @JvmStatic
    fun main(args: Array<String>) {
        expect("measurement requires a prior prediction") {
            val failed = runCatching { EpisodeState().confirmMeasurement(Trial.FLAT, 3, 0) }
            check(failed.isFailure)
        }
        expect("duplicate prediction is idempotent") {
            val once = EpisodeState().commitPrediction(Trial.FLAT.predictionKey, "flat", 0)
            check(once.commitPrediction(Trial.FLAT.predictionKey, "flat", 0) == once)
            check(runCatching { once.commitPrediction(Trial.FLAT.predictionKey, "folded", 1) }.isFailure)
        }
        expect("adult-confirmed correction drives exact scene value") {
            val state = stateWithBothPredictions().confirmMeasurement(Trial.FLAT, 4, 2)
            check(state.flatResultSceneParameters()["load_count"] == 4)
        }
        expect("greater branch uses confirmed values") {
            val state = stateWithBothPredictions()
                .confirmMeasurement(Trial.FLAT, 3, 2)
                .confirmMeasurement(Trial.FOLDED, 7, 3)
            check(state.comparison() == ComparisonResult.GREATER)
            check(state.measuredSummary().flatLoad == 3)
            check(state.measuredSummary().foldedLoad == 7)
        }
        expect("equal branch is deterministic") {
            val state = stateWithBothPredictions()
                .confirmMeasurement(Trial.FLAT, 4, 2)
                .confirmMeasurement(Trial.FOLDED, 4, 3)
            check(state.comparison() == ComparisonResult.EQUAL)
        }
        expect("lower branch is deterministic") {
            val state = stateWithBothPredictions()
                .confirmMeasurement(Trial.FLAT, 6, 2)
                .confirmMeasurement(Trial.FOLDED, 2, 3)
            check(state.comparison() == ComparisonResult.LOWER)
        }
        expect("duplicate confirmation creates no second transition") {
            val state = stateWithBothPredictions().confirmMeasurement(Trial.FLAT, 4, 2)
            val duplicate = state.confirmMeasurement(Trial.FLAT, 4, 2)
            check(duplicate == state)
            check(duplicate.stateSequence == 3L)
            check(runCatching { state.confirmMeasurement(Trial.FLAT, 5, 3) }.isFailure)
        }
        expect("stale and out-of-range confirmations fail") {
            val state = stateWithBothPredictions()
            check(runCatching { state.confirmMeasurement(Trial.FLAT, 4, 1) }.isFailure)
            check(runCatching { state.confirmMeasurement(Trial.FLAT, 101, 2) }.isFailure)
        }
        expect("summary cannot bypass committed prerequisites") {
            check(runCatching { EpisodeState().measuredSummary() }.isFailure)
            check(runCatching { stateWithBothPredictions().measuredSummary() }.isFailure)
        }
        expect("resumed committed state does not replay completion") {
            val committed = stateWithBothPredictions()
                .confirmMeasurement(Trial.FLAT, 0, 2)
                .confirmMeasurement(Trial.FOLDED, 100, 3)
            val resumed = committed.copy()
            check(resumed.measuredSummary() == committed.measuredSummary())
            check(resumed.confirmMeasurement(Trial.FOLDED, 100, 3) == resumed)
        }
        println("PASS $passed Kotlin episode-engine tests")
    }
}
