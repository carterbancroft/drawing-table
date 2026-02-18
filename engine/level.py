import json


class Level:
    def __init__(self, data_path) -> None:
        with open(data_path, "r") as f:
            self.data = json.load(f)
            self.layers = sorted(self.data["layers"], key=lambda l: l["z_index"])

        self.width = len(self.layers[0]["tile_map"][0]) * self.data["tile_size"]
        self.height = len(self.layers[0]["tile_map"]) * self.data["tile_size"]

    def get_solid_layers(self):
        return [l for l in self.layers if l["solid"]]
