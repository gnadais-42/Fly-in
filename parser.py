from webcolors import name_to_hex
from simulation import Graph, Node, Edge

class ParsingError(Exception):
    pass

class Parser:
    nb_drones: int = 0
    start: str = ""
    end: str = ""
    zones: dict[str, dict] = {}
    connections: dict[str, list[tuple[str, int]]] = {}

    @staticmethod
    def is_empty(line: str) -> bool:
        return line.strip() == ""
    
    @staticmethod
    def is_color(color: str) -> bool:
        try:
            name_to_hex(color)
            return True
        except ValueError:
            return False
    
    @classmethod
    def parse_file(cls, filename: str) -> None:
        try:
            with open(filename) as f:
                n_line: int = 1
                first_line: str = f.readline()
                cls.parse_first_line(first_line)
                n_line += 1
                for line in f:
                    if line.startswith("#"):
                        n_line += 1
                        continue
                    elif cls.is_empty(line):
                        n_line += 1
                        continue
                    elif line.startswith("hub:"):
                        cls.parse_hub(line, "hub")
                    elif line.startswith("connection:"):
                        cls.parse_connection(line)
                    elif line.startswith("start_hub:"):
                        if cls.start != "":
                            raise ParsingError("Start hub can't be defined more than once")
                        cls.start = cls.parse_hub(line, "start_hub")
                    elif line.startswith("end_hub:"):
                        if cls.end != "":
                            raise ParsingError("End hub can't be defined more than once")
                        cls.end = cls.parse_hub(line, "end_hub")
                    else:
                        raise ParsingError("Unknown beginning of line")
                    n_line += 1
        except (FileNotFoundError, PermissionError) as e:
            print(e)
            return
        except ParsingError as e:
            print(f"Parsing Error on line {n_line}:", e)
            return
    
    @classmethod
    def parse_first_line(cls, line: str) -> None:
        prefix, value = line.split(":", 1)
        if prefix.strip() != "nb_drones":
            raise ParsingError("First line must be of format "
                               "'nb_drones: <number of drones>'")
        try:
            cls.nb_drones = int(value.strip())
        except ValueError:
            raise ParsingError("First line must be of format "
                               "'nb_drones: <number of drones>'")
        
    @classmethod
    def parse_hub(cls, line: str, prefix: str) -> str:
        line = line.strip()
        attributes: list[str] = [s for s in line.split(" ") if s != ""]
        if len(attributes) < 4:
            raise ParsingError(f"{prefix} lines must be in format '{prefix}: <name> <x coordinate>"
                               " <y coordinate> <[modifiers], optional>'")
        if "-" in attributes[1]:
            raise ParsingError("Hub names can't have the character '-'")
        if len(attributes) > 4:
            if not attributes[4].startswith("[") or not attributes[-1].endswith("]"):
                raise ParsingError(f"Hub lines must be in format '{prefix}: <name> <x coordinate>"
                                   " <y coordinate> <[modifiers], optional>'")
            attributes[4] = attributes[4].removeprefix("[")
            attributes[-1] = attributes[-1].removesuffix("]")
        try:
            coordinates = (int(attributes[2]), int(attributes[3]))
            if attributes[1] in cls.zones:
                raise ParsingError(f"Hub '{attributes[1]}' can't be defined more than once")
            cls.zones[attributes[1]] = {"coordinates": coordinates}
        except ValueError:
            raise ParsingError("Coordinates must be valid integers")
        modifiers = attributes[4::]
        cls.parse_hub_mods(modifiers, cls.zones[attributes[1]])
        if prefix == "start_hub" or prefix == "end_hub":
            cls.zones[attributes[1]]["max_drones"] = None
        return(attributes[1])

    @staticmethod
    def parse_hub_mods(modifiers: list[str], hub: dict) -> None:
        for mod in modifiers:
            k_v: list[str] = mod.split("=")
            if len(k_v) != 2:
                raise ParsingError("Hub modifiers must be in format <type=mod>")
            if hub.get(k_v[0], None) is not None:
                raise ParsingError(f"Multiple definition of {k_v[0]} modifier")
            if k_v[0] == "zone":
                if k_v[1] not in ("normal", "restricted", "priority", "blocked"):
                    raise ParsingError(f"Invalid zone '{k_v[1]}'")
                hub["zone"] = k_v[1]
            elif k_v[0] == "color":
                if not Parser.is_color(k_v[1]):
                    raise ParsingError(f"'{k_v[1]}' is not a valid color")
                hub["color"] = k_v[1]
            elif k_v[0] == "max_drones":
                try:
                    n = int(k_v[1])
                    if n <= 0:
                        raise ParsingError("max_drones must be a positive integer")
                except ValueError:
                    raise ParsingError(f"'{k_v[1]}' is not a valid integer for max_drones")
                hub["max_drones"] = n
            else:
                raise ParsingError(f"Invalid modifier '{k_v[0]}'")
        if hub.get("zone", None) is None:
            hub["zone"] = "normal"
        if hub.get("color", None) is None:
            hub["color"] = "gray"
        if hub.get("max_drones", None) is None:
            hub["max_drones"] = 1
        
    @classmethod
    def parse_connection(cls, line: str) -> None:
        line = line.strip()
        attributes: list[str] = [s for s in line.split(" ") if s != ""]
        if len(attributes) < 2 or len(attributes) > 3:
            raise ParsingError("Connection lines should be in format 'connection: "
                               "<hub-hub> <[modifiers], optional>'")
        zones: list[str] = attributes[1].split("-")
        if len(zones) != 2:
            raise ParsingError("Connection lines should be in format 'connection: "
                               "<hub-hub> <[modifiers], optional>'")
        zone1 = zones[0]
        zone2 = zones[1]
        max_link = 1
        if zone1 not in cls.zones:
            raise ParsingError(f"Hub '{zone1}' is not defined")
        if zone2 not in cls.zones:
            raise ParsingError(f"Hub '{zone2}' is not defined")
        if cls.connections.get(zone1) is None:
            cls.connections[zone1] = []
        if cls.connections.get(zone2) is None:
            cls.connections[zone2] = []
        for connection in cls.connections[zone1]:
            if connection[0] == zone2:
                raise ParsingError(f"Connection '{attributes[1]}' is already established")
        if len(attributes) == 3:
            if not attributes[2].startswith("[") or not attributes[2].endswith("]"):
                raise ParsingError("Connection lines must be in format 'hub: <name> <x coordinate>"
                                   " <y coordinate> <[modifiers], optional>'")
            attributes[2] = attributes[2].removeprefix("[")
            attributes[2] = attributes[2].removesuffix("]")
            mods = attributes[2].split("=")
            if len(mods) != 2:
                raise ParsingError("Connection modifiers must be in format <type=mod>")
            if mods[0] != "max_link_capacity":
                raise ParsingError(f"Invalid modification '{mods[0]}'")
            try:
                max_link = int(mods[1])
                if max_link <= 0:
                    raise ParsingError("Max link capacity should be a positive integer")
            except ValueError:
                raise ParsingError(f"'{mods[1]}' is not a valid integer")
        cls.connections[zone1].append((zone2, max_link))
        cls.connections[zone2].append((zone1, max_link))


def create_simulation() -> Simulation:
    


if __name__ == "__main__":
    Parser.parse_file("test.txt")
    print("number of drones:", Parser.nb_drones if Parser.nb_drones != 0 else "N/A")
    print("start_hub:", Parser.start)
    print("end_hub:", Parser.end)
    print("zones:", Parser.zones)
    print("connections:", Parser.connections)
    