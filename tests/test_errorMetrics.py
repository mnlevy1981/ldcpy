import numpy as np
from unittest import TestCase
from ldcpy.error_metrics import ErrorMetrics


class TestErrorMetrics(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._samples = [
            {
                "measured": np.arange(0,100, dtype='int64'),
                "observed": np.arange(0,100, dtype='int64'),
                "expected_error": np.zeros(100, dtype="double")
            }
        ]

    def test_creation_01(self):
        ErrorMetrics(observed=self._samples[0]["observed"],
                     modelled=self._samples[0]["measured"])

    def test_error_01(self):
        em = ErrorMetrics(
            observed=self._samples[0]["observed"],
            modelled=self._samples[0]["measured"]
        )

        self.assertTrue(all(self._samples[0]["expected_error"] == em.error))

    def test_mean_error_01(self):
        em = ErrorMetrics(
            observed=self._samples[0]["observed"],
            modelled=self._samples[0]["measured"]
        )

        self.assertTrue(em.mean_error == 0.0)

    def test_mean_error_02(self):
        em = ErrorMetrics(
            observed=self._samples[0]["observed"],
            modelled=self._samples[0]["measured"]
        )

        self.assertTrue(em.mean_error == 0.0)

        em.mean_error = 42.0

        self.assertTrue(em.mean_error == 0.0)

    def test_get_all_metrics(self):
        em = ErrorMetrics(
            observed=self._samples[0]["observed"],
            modelled=self._samples[0]["measured"]
        )

        import json
        # print(em.get_all_metrics())
        print(json.dumps(em.get_all_metrics(), indent=4, separators=(",", ": ")))

        print(json.dumps(em.get_all_metrics({"error", "squared_error", "absolute_error"}), indent=4, separators=(",", ": ")))

    def test_TS_01(self):
        import xarray as xr
        import zfpy

        ds = xr.open_dataset('../data/orig.TS.100days.nc')
        TS = ds.TS.values
        TS_compressed = zfpy.compress_numpy(TS, tolerance=0.01)
        TS_decompressed = zfpy.decompress_numpy(TS_compressed)

        em = ErrorMetrics(observed=TS, modelled=TS_decompressed)
        print("mean squared error: ", em.mean_squared_error)

        em.get_all_metrics()
        print(em.get_all_metrics(exclude={"error", "squared_error", "absolute_error"}))

    def test_TS_02(self):
        import xarray as xr
        import zfpy

        ds = xr.open_dataset('../data/orig.TS.100days.nc')

        TS = ds.TS

        print(type(TS))