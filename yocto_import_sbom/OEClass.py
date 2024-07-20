import os
import requests
import json
import logging
import re
from semver import Version
from typing import Optional, Tuple

from . import global_values
from .RecipeClass import Recipe


class OE:
    def __init__(self):
        logging.info(f"Processing OE recipes and layers ...")
        self.layers = self.get_oe_layers()
        self.layerid_dict = self.process_layers()
        self.layerbranches = self.get_oe_layerbranches()
        self.layerbranchid_dict = self.process_layerbranches()
        self.recipes = self.get_oe_recipes()
        self.recipename_dict = self.process_recipes()
        self.branches = self.get_oe_branches()
        self.branchid_dict = self.process_branches()

    @staticmethod
    def get_oe_layers():
        oe_data_file_exists = False
        if global_values.oe_data_folder != '':
            lfile = os.path.join(global_values.oe_data_folder, 'oe_layers.json')
            if os.path.exists(lfile):
                oe_data_file_exists = True

        if not oe_data_file_exists:
            try:
                url = "https://layers.openembedded.org/layerindex/api/layerItems/"
                r = requests.get(url)
                if r.status_code != 200:
                    raise Exception(f"Status code {r.status_code}")

                layer_dict = json.loads(r.text)
                json_object = json.dumps(layer_dict, indent=4)

                if global_values.oe_data_folder != '':
                    # Writing to sample.json
                    with open(lfile, "w") as outfile:
                        outfile.write(json_object)

                return layer_dict

            except ConnectionError as e:
                logging.warning(f"Unable to connect to openembedded.org to get list of layers - error {e}")
        else:
            try:
                with open(lfile, "r") as infile:
                    return json.load(infile)

            except Exception as e:
                logging.warning(f"Error processing OE layers {e} from file - skipping")

        return {}

    @staticmethod
    def get_oe_recipes():
        oe_data_file_exists = False
        if global_values.oe_data_folder != '':
            lfile = os.path.join(global_values.oe_data_folder, 'oe_recipes.json')
            if os.path.exists(lfile):
                oe_data_file_exists = True

        lfile = 'oe_recipes.json'
        if not oe_data_file_exists:
            try:
                url = "https://layers.openembedded.org/layerindex/api/recipes"
                r = requests.get(url)
                if r.status_code != 200:
                    raise Exception(f"Status code {r.status_code}")

                recipe_dict = json.loads(r.text)
                json_object = json.dumps(recipe_dict, indent=4)

                if global_values.oe_data_folder != '':
                    # Writing to sample.json
                    with open(lfile, "w") as outfile:
                        outfile.write(json_object)

                return recipe_dict

            except ConnectionError as e:
                logging.warning(f"Unable to connect to openembedded.org to get list of recipes - error {e}")
        else:
            try:
                with open(lfile, "r") as infile:
                    recipe_dict = json.load(infile)
                return recipe_dict

            except Exception as e:
                logging.warning(f"Error processing OE recipes from file {e} - skipping")

        return {}

    @staticmethod
    def get_oe_layerbranches():
        oe_data_file_exists = False
        if global_values.oe_data_folder != '':
            lfile = os.path.join(global_values.oe_data_folder, 'oe_layerbranches.json')
            if os.path.exists(lfile):
                oe_data_file_exists = True

        if not oe_data_file_exists:
            try:
                url = "https://layers.openembedded.org/layerindex/api/layerBranches"
                r = requests.get(url)
                if r.status_code != 200:
                    raise Exception(f"Status code {r.status_code}")

                layerbranches_dict = json.loads(r.text)
                json_object = json.dumps(layerbranches_dict, indent=4)

                if global_values.oe_data_folder != '':
                    # Writing to sample.json
                    with open(lfile, "w") as outfile:
                        outfile.write(json_object)

                return layerbranches_dict

            except ConnectionError as e:
                logging.warning(f"Unable to connect to openembedded.org to get list of layerbranches - error {e}")
        else:
            try:
                with open(lfile, "r") as infile:
                    layerbranches_dict = json.load(infile)
                return layerbranches_dict

            except Exception as e:
                logging.warning(f"Error processing OE layerbranches from file {e} - skipping")

        return {}

    @staticmethod
    def get_oe_branches():
        oe_data_file_exists = False
        if global_values.oe_data_folder != '':
            lfile = os.path.join(global_values.oe_data_folder, 'oe_branches.json')
            if os.path.exists(lfile):
                oe_data_file_exists = True

        if not oe_data_file_exists:
            try:
                url = "https://layers.openembedded.org/layerindex/api/branches"
                r = requests.get(url)
                if r.status_code != 200:
                    raise Exception(f"Status code {r.status_code}")

                branches_dict = json.loads(r.text)
                json_object = json.dumps(branches_dict, indent=4)

                if global_values.oe_data_folder != '':
                    # Writing to sample.json
                    with open(lfile, "w") as outfile:
                        outfile.write(json_object)

                return branches_dict

            except ConnectionError as e:
                logging.warning(f"Unable to connect to openembedded.org to get list of branches - error {e}")
        else:
            try:
                with open(lfile, "r") as infile:
                    layerbranches_dict = json.load(infile)
                return layerbranches_dict

            except Exception as e:
                logging.warning(f"Error processing OE branches from file {e} - skipping")

        return {}

    def process_layers(self):
        try:
            layer_dict = {}
            for layer in self.layers:
                layer_dict[layer['id']] = layer
            return layer_dict
        except Exception as e:
            logging.warning(f"Cannot process layer {e}")

        return {}

    def process_recipes(self):
        try:
            recipe_dict = {}
            for recipe in self.recipes:
                if recipe['pn'] in recipe_dict.keys():
                    recipe_dict[recipe['pn']].append(recipe)
                else:
                    recipe_dict[recipe['pn']] = [recipe]
            return recipe_dict
        except Exception as e:
            logging.warning(f"Cannot process recipe {e}")
        return {}

    def process_layerbranches(self):
        try:
            layerbranch_dict = {}
            for layerbranch in self.layerbranches:
                layerbranch_dict[layerbranch['id']] = layerbranch
            return layerbranch_dict
        except Exception as e:
            logging.warning(f"Cannot process layerbranch {e}")
        return {}

    def process_branches(self):
        try:
            branch_dict = {}
            for branch in self.branches:
                branch_dict[branch['id']] = branch
            return branch_dict
        except Exception as e:
            logging.warning(f"Cannot process branch {e}")

        return {}

    def get_layer_by_layerbranchid(self, id):
        try:
            layerid = self.layerbranchid_dict[id]['layer']
            return self.layerid_dict[layerid]
        except KeyError as e:
            logging.warning(f"Cannot get layer by layerbranchid {e}")
        return {}

    def get_branch_by_layerbranchid(self, id):
        try:
            branchid = self.layerbranchid_dict[id]['branch']
            return self.branchid_dict[branchid]
        except KeyError as e:
            logging.warning(f"Cannot get branch by layerbranchid {e}")
        return {}

    def get_recipe(self, recipe):
        # Returns:
        # - recipe dict
        # - layer dict
        try:
            best_recipe = {}
            best_layer = {}
            best_layer_pref = -1
            best_branch_sort_priority = 999

            exact_recipe = {}
            exact_layer = {}
            exact_layer_pref = -1
            exact_branch_sort_priority = 999
            exact_match = False

            recipe_exists_in_oe = False
            if recipe.name in self.recipename_dict.keys():
                recipe_exists_in_oe = True
                for oe_recipe in self.recipename_dict[recipe.name]:
                    oe_layer = self.get_layer_by_layerbranchid(oe_recipe['layerbranch'])
                    oe_branch = self.get_branch_by_layerbranchid(oe_recipe['layerbranch'])
                    if oe_branch is not None and oe_branch['sort_priority'] is not None \
                            and str(oe_branch['sort_priority']).isnumeric():
                        branch_sort_priority = oe_branch['sort_priority']
                    else:
                        branch_sort_priority = 999

                    if oe_layer == {}:
                        continue

                    oe_ver = Recipe.filter_version_string(oe_recipe['pv'])
                    epoch_match = True
                    if recipe.epoch != '' and oe_recipe['pe'] != '' and recipe.epoch != oe_recipe['pe']:
                        # not an epoch match
                        epoch_match = False

                        # Exact match
                    if (epoch_match and oe_ver == recipe.version and epoch_match and
                            oe_layer['index_preference'] >= exact_layer_pref and
                            branch_sort_priority < exact_branch_sort_priority):
                        exact_recipe = oe_recipe
                        exact_layer = oe_layer
                        exact_layer_pref = oe_layer['index_preference']
                        exact_branch_sort_priority = branch_sort_priority
                        exact_match = True

                    if not exact_match:
                        # No exact match
                        ver_split = re.split(r"[+\-]", recipe.version)
                        oever_split = re.split(r"[+\-]", oe_ver)
                        if ver_split[0] == oever_split[0]:
                            if oe_layer['index_preference'] > best_layer_pref and oe_ver != '':
                                best_recipe = oe_recipe
                                best_layer = oe_layer
                                best_layer_pref = oe_layer['index_preference']
                                best_branch_sort_priority = branch_sort_priority

            if recipe.epoch != '':
                recipe_ver = f"{recipe.epoch}:{recipe.orig_version}"
            else:
                recipe_ver = recipe.orig_version

            if exact_match:
                best_recipe = exact_recipe
                best_layer = exact_layer

            if best_recipe != {}:
                if best_recipe['pe'] != '':
                    best_ver = f"{best_recipe['pe']}:{best_recipe['pv']}"
                else:
                    best_ver = best_recipe['pv']

                logging.debug(f"Recipe {recipe.name}: {recipe.layer}/{recipe.name}/{recipe_ver} - OE match "
                                  f"{best_layer['name']}/{best_recipe['pn']}/{best_ver}-{best_recipe['pr']}")
            else:
                if recipe_exists_in_oe:
                    return self.get_nearest_oe_recipe(recipe)

                logging.debug(f"Recipe {recipe.name}: {recipe.layer}/{recipe.name}/{recipe_ver} - "
                              f"Recipe does not exist in OE Data")
            return best_recipe, best_layer

        except KeyError as e:
            logging.warning(f"Cannot get recipe by name,version {e}")

        return {}, {}


    def get_nearest_oe_recipe(self, recipe):
        # No exact match found
        # need to look for closest version match

        logging.debug(f"Trying closest OE match for {recipe.name}/{recipe.version}")
        try:
            best_recipe = {}
            best_layer = {}
            best_distance = 999999

            if not Version.is_valid(recipe.version):
                rec_semver, rest = self.coerce(recipe.version)
            else:
                rec_semver = Version.parse(recipe.version)

            if recipe.name in self.recipename_dict.keys():
                for oe_recipe in self.recipename_dict[recipe.name]:
                    oe_layer = self.get_layer_by_layerbranchid(oe_recipe['layerbranch'])
                    # oe_branch = self.get_branch_by_layerbranchid(oe_recipe['layerbranch'])

                    if oe_layer == {} or oe_recipe['pv'] == '':
                        continue

                    oe_ver = Recipe.filter_version_string(oe_recipe['pv'])
                    if not Version.is_valid(oe_ver):
                        oe_semver, rest = self.coerce(oe_ver)
                    else:
                        oe_semver = Version.parse(oe_ver)

                    if oe_semver is None:
                        continue

                    distance = ((rec_semver.major - oe_semver.major) * 10000 + (rec_semver.minor - oe_semver.minor)
                                * 100 + (rec_semver.patch - oe_semver.patch))
                    if distance > 0 and distance < best_distance:
                        best_recipe = oe_recipe
                        best_layer = oe_layer
                        best_distance = distance

            if recipe.epoch != '':
                recipe_ver = f"{recipe.epoch}:{recipe.orig_version}"
            else:
                recipe_ver = recipe.orig_version

            if best_recipe != {}:
                if best_recipe['pe'] != '':
                    best_ver = f"{best_recipe['pe']}:{best_recipe['pv']}"
                else:
                    best_ver = best_recipe['pv']
            else:
                logging.debug(f"Recipe {recipe.name}: {recipe.layer}/{recipe.name}/{recipe_ver} - "
                              f"No close (previous) OE version match found")
                return {}, {}

            if best_distance > global_values.max_oe_version_distance:
                logging.debug(f"Recipe {recipe.name}: {recipe.layer}/{recipe.name}/{recipe_ver} - "
                              f"Recipe {best_layer['name']}/{best_recipe['pn']}/{best_ver}-{best_recipe['pr']} "
                              f"exists in OE data but distance {best_distance} exceeds specified max version "
                              f"distance {global_values.max_oe_version_distance}")
                return {}, {}

            logging.debug(f"Recipe {recipe.name}: {recipe.layer}/{recipe.name}/{recipe_ver} - OE near match "
                          f"{best_layer['name']}/{best_recipe['pn']}/{best_ver}-{best_recipe['pr']} - "
                          f"(Distance {best_distance})")

            return best_recipe, best_layer

        except KeyError as e:
            logging.warning(f"Error getting nearest OE recipe - {e}")

    @staticmethod
    def coerce(version: str) -> Tuple[Version, Optional[str]]:
        """
        Convert an incomplete version string into a semver-compatible Version
        object

        * Tries to detect a "basic" version string (``major.minor.patch``).
        * If not enough components can be found, missing components are
            set to zero to obtain a valid semver version.

        :param str version: the version string to convert
        :return: a tuple with a :class:`Version` instance (or ``None``
            if it's not a version) and the rest of the string which doesn't
            belong to a basic version.
        :rtype: tuple(:class:`Version` | None, str)
        """
        BASEVERSION = re.compile(
            r"""[vV]?
                (?P<major>0|[1-9]\d*)
                (\.
                (?P<minor>0|[1-9]\d*)
                (\.
                    (?P<patch>0|[1-9]\d*)
                )?
                )?
            """,
            re.VERBOSE,
        )

        match = BASEVERSION.search(version)
        if not match:
            return (None, version)

        ver = {
            key: 0 if value is None else value for key, value in match.groupdict().items()
        }
        ver = Version(**ver)
        rest = match.string[match.end():]  # noqa:E203
        return ver, rest
