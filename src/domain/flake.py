from domain.entity import Entity, primary_key_attribute, attribute
from domain.event import Event
from domain.event_listener import EventListener
from domain.create_flake import CreateFlake
from domain.flake_requested import FlakeRequested
from domain.python_package import PythonPackage
from domain.python_package_repo import PythonPackageRepo
from domain.git_repo import GitRepo
from domain.git_repo_repo import GitRepoRepo
from domain.nix_python_package_repo import NixPythonPackageRepo
from domain.nix_template import NixTemplate
from domain.ports import Ports

from typing import Dict, List, Type
import logging

class Flake(Entity, EventListener):

    """
    Represents a nix flake.
    """
    def __init__(self, name: str, version: str, pythonPackage: PythonPackage, nativeBuildInputs: List, propagatedBuildInputs: List, checkInputs: List, optionalBuildInputs: List, dependenciesInNixpkgs: List):
        """Creates a new flake instance"""
        super().__init__(id)
        self._name = name
        self._version = version
        self._python_package = pythonPackage
        self._native_build_inputs = nativeBuildInputs
        self._propagated_build_inputs = propagatedBuildInputs
        self._check_inputs = checkInputs
        self._optional_build_inputs = optionalBuildInputs
        self._dependencies_in_nixpkgs = dependenciesInNixpkgs

    @property
    @primary_key_attribute
    def name(self) -> str:
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        return self._version

    @property
    @attribute
    def python_package(self) -> PythonPackage:
        return self._python_package

    @property
    @attribute
    def native_build_inputs(self) -> List:
        return self._native_build_inputs

    @property
    @attribute
    def propagated_build_inputs(self) -> List:
        return self._propagated_build_inputs

    @property
    @attribute
    def check_inputs(self) -> List:
        return self._check_inputs

    @property
    @attribute
    def optional_build_inputs(self) -> List:
        return self._optional_build_inputs

    @property
    @attribute
    def dependencies_in_nixpkgs(self) -> List:
        return self._dependencies_in_nixpkgs

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        return [ FlakeRequested ]

    def listenFlakeRequested(self, event: FlakeRequested): # -> FlakeCreated:
        result = None
        logger = logging.getLogger(__name__)
        logger.info(f'Received "flake requested {event.packageName}-{event.packageVersion}"')
        flakeRepo = Ports.instance().resolveFlakeRepo()
        # 1. check if flake exists already
        existingFlake = flakeRepo.find_by_name_and_version(event.packageName, event.packageVersion)
        if existingFlake:
            logger.info(f'flake ({event.packageName}, {event.packageVersion}) already exists')
        else:
            # 2. obtain pypi info
            pythonPackage = Ports.instance().resolve(PythonPackageRepo).find_by_name_and_version(event.packageName, event.packageVersion)

            nixPythonPackageRepo = Ports.instance().resolve(NixPythonPackageRepo)
            nativeBuildInputs = pythonPackage.get_native_build_inputs()
            propagatedBuildInputs = pythonPackage.get_propagated_build_inputs()
            checkInputs = pythonPackage.get_check_inputs()
            optionalBuildInputs = pythonPackage.get_optional_build_inputs()
            dependenciesInNixpkgs = []
            for dep in list(set(nativeBuildInputs) | set(propagatedBuildInputs) | set(checkInputs) | set(optionalBuildInputs)):
                depName = dep.name
                depVersion = dep.version
                nixPythonPackages = nixPythonPackageRepo.find_by_name(dep.name)
                if len(nixPythonPackages) > 0:
                    nixPythonPackage = nixPythonPackages[len(nixPythonPackages) - 1]
                    if pythonPackage.satisfies_spec(nixPythonPackage.version):
                        dependenciesInNixpkgs.append(pythonPackage)
                        depName = nixPythonPackage.name
                        depVersion = nixPythonPackage.version
                # check if there's a flake for the dependency
                depFlake = flakeRepo.find_by_name_and_version(depName, depVersion)
                if depFlake:
                    logger.debug(f'Flake found for {depName}-{depVersion}')
                else:
                    flakeCreated = cls.create_flake(CreateFlake(depName, depVersion))
                    logger.info(f'Flake {dep.name}-{dep.version} created (triggered by "create flake {event.packageName}-{event.packageVersion}")')

            # 3. create flake
            flake = Flake(event.packageName, event.packageVersion, pythonPackage, nativeBuildInputs, propagatedBuildInputs, checkInputs, optionalBuildInputs, dependenciesInNixpkgs)
            flakeRecipe = cls.find_recipe_by_flake(flake)
            if flakeRecipe:
                result = flakeRecipe.process()

            else:
                logger.critical(f'No recipe available for {event.packageName}-{event.packageVersion}')

            if result:
                logger.info(f'Flake {event.packageName}-{event.packageVersion} created')
            else:
                logger.info(f'Flake {event.packageName}-{event.packageVersion} could not be created')

        return result

    def find_recipe_by_flake(self, flake):
        """
        Retrieves the best recipe for given Flake
        """
        result = None
        flakeRecipeClasses = Ports.instance().resolveFlakeRecipeRepo().find_recipe_classes_by_flake(flake)
        similarities = {}
        for recipeClass in flakeRecipeClasses:
            similarities[recipeClass] = recipeClass.similarity(flake)
        matches = sorted([aux for aux in similarities.keys() if similarities[aux] != 0.0], key=lambda recipeClass: similarities[recipeClass], reverse=True)
        if matches and len(matches) > 0:
            result = matches[0](flake)
        return result

    def dependency_in_nixpkgs(self, dep: PythonPackage) -> bool:
        """
        Checks if given dependency is already in nixpkgs.
        """
        nixPythonPackageRepo = Ports.instance().resolveNixPythonPackageRepo()
        result = nixPythonPackageRepo.find_by_name_and_version(dep.name, dep.version) == None
        if not result:
            existing = nixPythonPackageRepo.find_by_name(dep.name)
            result = existing and len(existing) > 0 and any(pkg.is_compatible_with(self.version) for pkg in existing)
        return result
