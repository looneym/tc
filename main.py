from mcpack import DataPack, Function

SINGLE_CHEST_SIZE = 27
DOUBLE_CHEST_SIZE = 54

class ContributionMainFunction:
    def __init__(
        self,
        input_chest_coords,
        reward_block_coords,
        item_storage_block_coords,
        item_id,
        chest_size,
        stack_size,
        namespace,
        reward_item_id,
        reward_item_count,
    ):
        self.input_chest_coords = input_chest_coords
        self.reward_block_coords = reward_block_coords
        self.item_storage_block_coords = item_storage_block_coords
        self.item_id = item_id
        self.chest_size = chest_size
        self.stack_size = stack_size
        self.namespace = namespace
        self.reward_item_id = reward_item_id
        self.reward_item_count = reward_item_count

        self.body_list = []
        self.sub_functions = []

        for i in range(self.chest_size):
            self.body_list.append(self.sub_function_call(i))
            self.sub_functions.append(self.create_sub_function(i))

    def sub_function_call(self, index):
        x = self.input_chest_coords["x"]
        y = self.input_chest_coords["y"]
        z = self.input_chest_coords["z"]

        return (
            f"execute if block {x} {y} {z} chest{{Items:[{{Slot:{index}b,id:"
            f"{self.item_id}"
            f",Count:{self.stack_size}b}}]}} run function contribute:{self.namespace}/{index}"
        )

    def generate_function(self):
        return Function(self.generate_body())

    def generate_body(self):
        return "\n".join(self.body_list)

    def create_sub_function(self, index):
        return ContributionSubFunction(
            index,
            self.item_id,
            self.stack_size,
            self.reward_block_coords,
            self.item_storage_block_coords,
            self.reward_item_id,
            self.reward_item_count,
        )


class ContributionSubFunction:
    def __init__(
        self,
        index,
        input_item_id,
        input_item_stack_size,
        reward_block_coords,
        item_storage_block_coords,
        reward_item_id,
        reward_item_count,
    ):
        self.index = index
        self.input_item_id = input_item_id
        self.input_item_stack_size = input_item_stack_size
        self.reward_block_coords = reward_block_coords
        self.item_storage_block_coords = item_storage_block_coords
        self.reward_item_id = reward_item_id
        self.reward_item_count = reward_item_count

        self.body_list = []

        self.body_list.append(self.reward_command())
        self.body_list.append(self.delete_command())
        self.body_list.append(self.transport_command())

    def reward_command(self):
        x = self.reward_block_coords["x"]
        y = self.reward_block_coords["y"]
        z = self.reward_block_coords["z"]

        return (
            f"summon item {x} {y} {z} {{Item:{{Count:{self.reward_item_count}b,id:"
            f"{self.reward_item_id}"
            f"}}}}"
        )

    def delete_command(self):
        x = self.reward_block_coords["x"]
        y = self.reward_block_coords["y"]
        z = self.reward_block_coords["z"]

        return f"replaceitem block {x} {y} {x} container.{self.index} minecraft:air 1"

    def transport_command(self):
        x = self.item_storage_block_coords["x"]
        y = self.item_storage_block_coords["y"]
        z = self.item_storage_block_coords["z"]

        return (
            f"summon item {x} {y} {z} {{Item:{{Count:{self.input_item_stack_size}b,id:"
            f"{self.input_item_id}"
            f"}}}}"
        )

    def generate_function(self):
        return Function(self.generate_body())

    def generate_body(self):
        return "\n".join(self.body_list)


pack = DataPack("trotskycraft-utils", "Utilities for the TrotskyCraft minecraft server")


# These values are hard-coded for now, but should be defined in a yaml file and read in on build
namespace = "cobble"
cobble = ContributionMainFunction(
    {
        "x": 47,
        "y": 56,
        "z": 19,
    },
    {
        "x": 47,
        "y": 58,
        "z": 18,
    },
    {
        "x": 47,
        "y": 58,
        "z": 17,
    },
    "minecraft:cobblestone",
    DOUBLE_CHEST_SIZE,
    64,
    namespace,
    "minecraft:diamond",
    1,
)

main_function = cobble.generate_function()
sub_functions = cobble.sub_functions

pack[f"contribute:{namespace}"] = main_function
for index, function in enumerate(sub_functions):
    pack[f"contribute:{namespace}:{index}"] = function.generate_function()

pack.dump("./out", overwrite=True)
