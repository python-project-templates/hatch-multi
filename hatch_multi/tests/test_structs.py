from hatch_multi.structs import HatchMultiConfig


class TestStructs:
    def test_config(self):
        config = HatchMultiConfig(name="test", primary="default")
        assert config.primary == "default"

        config = HatchMultiConfig(name="test", default="default")
        assert config.primary == "default"
