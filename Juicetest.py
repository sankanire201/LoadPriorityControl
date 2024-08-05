# Class to convert user uploaded master excel files to master dictionaries used by the optimisation model.

import os
import pandas as pd
import random


class DataProcessorinterface(ABC):
    @abstractmethod
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        pass


class DataProcessor(DataProcessorinterface):
    """
    A class used to convert various types of Excel files to dictionaries.

    Methods
    -------
    bf_freight_costs_to_dict(file_name)
        Converts an Excel file to a BF freight costs dictionary.

    variable_production_cost_to_dict(file_name)
        Converts an Excel file to a variable production cost dictionary.

    manufacturing_capacity_to_dict(file_name)
        Converts an Excel file to a manufacturing capacity dictionary.

    units_to_pallets_to_dict(file_name)
        Converts an Excel file to a units to pallets dictionary.

    create_freight_dict(file_name)
        Converts an Excel file to a freight dictionary and processes name mappings.

    save_dict_to_py(data_dict, file_name, header_comment, var_name)
        Saves a dictionary to a Python file with comments.
    """

    def bf_freight_costs_to_dict(self, file_name):
        """
        Converts an Excel file to a BF freight costs dictionary.

        Parameters:
        file_name (str): Name of the Excel file to read.

        Returns:
        dict: Dictionary containing the Excel data.
        """
        df = pd.read_excel(file_name)
        data_dict = {
            (
                row["LatestPartNbr"],
                row["PartType"],
                row["FromLocation"],
                row["ToLocation"],
            ): row["FreightCost"]
            for _, row in df.iterrows()
        }
        return data_dict

    def variable_production_cost_to_dict(self, file_name):
        """
        Converts an Excel file with columns Location, PartType, and VarCost to a nested dictionary.

        Parameters:
        file_name (str): Name of the Excel file to read.

        Returns:
        dict: Nested dictionary containing the Excel data.
        """
        df = pd.read_excel(file_name)
        data_dict = {}
        for _, row in df.iterrows():
            location = row["Location"]
            parttype = row["PartType"]
            cost = row["VarCost"]
            if location not in data_dict:
                data_dict[location] = {}
            data_dict[location][parttype] = cost
        return data_dict

    def manufacturing_capacity_to_dict(self, file_name):
        """
        Converts an Excel file with columns Location, PartType, and Capability to a nested dictionary.

        Parameters:
        file_name (str): Name of the Excel file to read.

        Returns:
        dict: Nested dictionary containing the Excel data.
        """
        df = pd.read_excel(file_name)
        data_dict = {}
        for _, row in df.iterrows():
            location = row["Location"]
            parttype = row["RootPartType"]
            capacity = row["Capacity"]
            if location not in data_dict:
                data_dict[location] = {}
            data_dict[location][parttype] = capacity
        return data_dict

    def units_to_pallets_to_dict(self, file_name):
        """
        Converts an Excel file with columns PartNumber, PartType, MUnitsPerCase, and CasesPerPallet to a nested dictionary.

        Parameters:
        file_name (str): Name of the Excel file to read.

        Returns:
        dict: Nested dictionary containing the Excel data.
        """
        df = pd.read_excel(file_name)
        data_dict = {}
        for _, row in df.iterrows():
            partnumber = row["PartNumber"]
            parttype = row["PartType"]
            munits_per_case = row["MUnitsPerCase"]
            cases_per_pallet = row["CasesPerPallet"]
            data_dict[(partnumber, parttype)] = (munits_per_case, cases_per_pallet)
        return data_dict

    def create_freight_dict(self, file_name):
        """
        Create a dictionary with keys as (ShipSite, ShipToState, ShipToCity, ProcessedShipToName, ShipToCountry)
        and values as corresponding DatFreightperMUnits_x from the df_freight DataFrame.

        Parameters:
        file_name (str): Name of the Excel file to read.

        Returns:
        tuple: A tuple containing the freight dictionary, name mapping dictionary, and inverse name mapping dictionary.
        """
        df_freight = pd.read_excel(file_name)
        df_freight.drop_duplicates(inplace=True)

        df_freight["MSTName"] = df_freight["MSTName"] + df_freight["Type"]
        df_freight.drop("Type", axis=1, inplace=True)

        name_mapping = {}
        inverse_name_mapping = {}
        suffix_tracker = {}

        def process_ship_to_name(name):
            processed_name_base = (
                name.lower().replace(" ", "").translate(str.maketrans("", "", ".,_-'/"))
            )
            if name not in suffix_tracker:
                while True:
                    suffix = random.randint(1000, 9999)
                    if suffix not in suffix_tracker.values():
                        suffix_tracker[name] = suffix
                        break
            else:
                suffix = suffix_tracker[name]
            processed_name_with_suffix = f"{processed_name_base}{suffix}"
            name_mapping[processed_name_with_suffix] = name
            inverse_name_mapping[name] = processed_name_with_suffix
            return processed_name_with_suffix

        df_freight["ProcessedShipToName"] = df_freight["MSTName"].apply(
            process_ship_to_name
        )
        df_freight["OriginalShipToName"] = df_freight["ProcessedShipToName"].apply(
            lambda x: name_mapping.get(x, x)
        )

        freight_dict = {
            (
                row["ShipSite"],
                row["MSTState"],
                row["MSTCity"],
                row["ProcessedShipToName"],
                row["MSTCountry"],
            ): row["DatFreight_PerMUnits"]
            for _, row in df_freight.iterrows()
        }
        return freight_dict, name_mapping, inverse_name_mapping

    def save_dict_to_py(
        self, data_dict, file_name, directory, header_comment, var_name
    ):
        """
        Saves a dictionary to a Python file with comments.

        Parameters:
        data_dict (dict): Dictionary to save.
        file_name (str): Name of the Python file to save.
        header_comment (str): Comment to add at the top of the file.
        var_name (str): Variable name for the dictionary.
        """
        os.makedirs(directory, exist_ok=True)
        full_path = os.path.join(directory, file_name)
        print("full path", full_path)
        with open(full_path, "w") as f:
            f.write(f"# {header_comment}\n")
            f.write(f"{var_name} = " + str(data_dict))


if __name__ == "__main__":
    converter = ExcelToDictConverter()
    test_files = {
        "bf_freight": "test_data/BF_freight_costs_PartNbr.xlsx",
        "variable_production_cost": "test_data/variable_production_cost_PartType.xlsx",
        "manufacturing_capacity": "test_data/manufacturing_capacity23_rootparttype.xlsx",
        "units_to_pallets": "test_data/Units_To_Pallets_parttype.xlsx",
        "freight": "test_data/DATFreight_MUnits_TypeMST.xlsx",
    }
    header_comments = {
        "bf_freight": "This file contains the BF_freight_costs dictionary converted from Excel",
        "variable_production_cost": "This file contains the variable_production_cost dictionary converted from Excel",
        "manufacturing_capacity": "This file contains the manufacturing_capacity dictionary converted from Excel",
        "units_to_pallets": "This file contains the units_to_pallets dictionary converted from Excel",
        "freight": "This file contains the freight_name_dict dictionary converted from Excel",
    }

    var_names = {
        "bf_freight": "BF_freight_costs",
        "variable_production_cost": "variable_production_cost",
        "manufacturing_capacity": "manufacturing_capacity",
        "units_to_pallets": "Units_To_Pallets",
        "freight": "freight_name_dict",
    }
    file_path = test_files["variable_production_cost"]
    output_directory = "../unittests_outputs"

    if os.path.isfile(file_path):
        data_dict = converter.variable_production_cost_to_dict(file_path)
        assert isinstance(data_dict, dict), "data_dict should be a dictionary"
        converter.save_dict_to_py(
            data_dict,
            "variable_production_cost_PartType.py",
            output_directory,
            header_comments["variable_production_cost"],
            var_names["variable_production_cost"],
        )
    else:
        print(f"File '{file_path}' does not exist.")
