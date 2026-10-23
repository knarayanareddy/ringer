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

    private fun manualFlatConfirmed(): ManualEpisodeSession {
        val session = ManualEpisodeSession()
        session.acknowledgeSafety(true, true, true, 0)
        session.commitPrediction(Trial.FLAT, "folded", 1)
        session.markStop(Trial.FLAT, 5, 2)
        session.confirmStoppedMeasurement(Trial.FLAT, 4, 3)
        return session
    }

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
        expect("manual consent stop and correction gate the exact scene value") {
            val session = ManualEpisodeSession()
            session.acknowledgeSafety(false, true, true, 0)
            check(session.snapshot.stage == ManualStage.SAFETY_AND_CONSENT)
            check(runCatching { session.commitPrediction(Trial.FLAT, "folded", 0) }.isFailure)
            session.acknowledgeSafety(true, true, true, 0)
            session.commitPrediction(Trial.FLAT, "folded", 1)
            check(runCatching { session.flatResultSceneParameters() }.isFailure)
            check(runCatching { session.confirmStoppedMeasurement(Trial.FLAT, 4, 2) }.isFailure)
            session.markStop(Trial.FLAT, 5, 2)
            session.confirmStoppedMeasurement(Trial.FLAT, 4, 3)
            check(session.flatResultSceneParameters()["load_count"] == 4)
            check(session.snapshot.stoppedMeasurements.getValue(Trial.FLAT).lastStableCount == 5)
        }
        expect("manual snapshot resumes and completes with measured reflection") {
            val resumed = ManualEpisodeSession(manualFlatConfirmed().snapshot)
            check(resumed.snapshot.stage == ManualStage.FOLDED_PREDICTION)
            resumed.commitPrediction(Trial.FOLDED, "more", 4)
            resumed.markStop(Trial.FOLDED, 2, 5)
            resumed.confirmStoppedMeasurement(Trial.FOLDED, 2, 6)
            resumed.acknowledgeComparison(7)
            resumed.commitReflection("shape_can_matter", 8)
            val summary = resumed.measuredSummary()
            check(summary.flatLoad == 4 && summary.foldedLoad == 2)
            check(summary.comparison == ComparisonResult.LOWER)
            check(summary.foldedPredictionMatched == false)
            check(summary.variableChangePrompt.contains("one comparison"))
            check(resumed.snapshot.sequence == 9L)
        }
        expect("manual duplicate stop and confirmation are idempotent") {
            val session = ManualEpisodeSession()
            session.acknowledgeSafety(true, true, true, 0)
            session.commitPrediction(Trial.FLAT, "same", 1)
            session.markStop(Trial.FLAT, 3, 2)
            val stopped = session.snapshot
            check(session.markStop(Trial.FLAT, 3, 2) == stopped)
            check(runCatching { session.markStop(Trial.FLAT, 4, 3) }.isFailure)
            session.confirmStoppedMeasurement(Trial.FLAT, 3, 3)
            val confirmed = session.snapshot
            check(session.confirmStoppedMeasurement(Trial.FLAT, 3, 3) == confirmed)
        }
        expect("manual stale sequences and out-of-range counts fail") {
            val session = manualFlatConfirmed()
            check(runCatching { session.commitPrediction(Trial.FOLDED, "more", 3) }.isFailure)
            session.commitPrediction(Trial.FOLDED, "more", 4)
            check(runCatching { session.markStop(Trial.FOLDED, 31, 5) }.isFailure)
            session.markStop(Trial.FOLDED, 7, 5)
            check(runCatching { session.confirmStoppedMeasurement(Trial.FOLDED, 7, 4) }.isFailure)
            check(runCatching { session.acknowledgeComparison(6) }.isFailure)
        }
        expect("manual summary requires the completed reflection") {
            check(runCatching { manualFlatConfirmed().measuredSummary() }.isFailure)
        }
        println("PASS $passed Kotlin episode-engine tests")
    }
}
