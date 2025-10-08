import json


class Level:
    def __init__(self, data_path) -> None:
        with open(data_path, "r") as f:
            self.data = json.load(f)
            self.layers = sorted(self.data["layers"], key=lambda l: l["z_index"])

    def get_solid_layers(self):
        return [l for l in self.layers if l["solid"]]
