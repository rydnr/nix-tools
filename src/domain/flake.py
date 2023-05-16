from domain.entity import Entity, primary_key_attribute, attribute
from domain.event import Event
from domain.event_emitter import EventEmitter
from domain.event_listener import EventListener
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

class Flake(Entity, EventListener, EventEmitter):

    """
    Represents a nix flake.
    """
    def __init__(self, name: str, version: str, pythonPackage: PythonPackage, nativeBuildInputs: List, propagatedBuildInputs: List, buildInputs: List, checkInputs: List, optionalBuildInputs: List):
        """Creates a new flake instance"""
        super().__init__()
        self._name = name
        self._version = version
        self._python_package = pythonPackage
        self._native_build_inputs = nativeBuildInputs
        self._propagated_build_inputs = propagatedBuildInputs
        self._build_inputs = buildInputs
        self._check_inputs = checkInputs
        self._optional_build_inputs = optionalBuildInputs

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
    def build_inputs(self) -> List:
        return self._build_inputs

    @property
    @attribute
    def check_inputs(self) -> List:
        return self._check_inputs

    @property
    @attribute
    def optional_build_inputs(self) -> List:
        return self._optional_build_inputs

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        return [ FlakeRequested ]

    @classmethod
    async def listenFlakeRequested(cls, event: FlakeRequested): # -> FlakeCreated:
        result = None
        logger = logging.getLogger(__name__)
        logger.info(f'Received "flake requested for {event.package_name}-{event.package_version}"')
        flakeRepo = Ports.instance().resolveFlakeRepo()

        logging.getLogger('step-by-step').info(f'Checking if there is a flake for {event.package_name}-{event.package_version}')
        existingFlake = flakeRepo.find_by_name_and_version(event.package_name, event.package_version)
        if existingFlake:
            logger.info(f'Flake for {event.package_name}-{event.package_version} already exists')
        else:
            logging.getLogger('step-by-step').info(f'Retrieving the Python package for {event.package_name}-{event.package_version}')
            pythonPackageRepo = Ports.instance().resolve(PythonPackageRepo)
            pythonPackage = await pythonPackageRepo.find_by_name_and_version(event.package_name, event.package_version)

            if pythonPackage:
                if pythonPackage.in_nixpkgs():
                    logger.info(f'Python package {pythonPackage.nixpkgs_package_name()} compatible with version {event.package_version} already exists in nixpkgs.')
                else:
                    nixPythonPackageRepo = Ports.instance().resolve(NixPythonPackageRepo)
                    logging.getLogger('step-by-step').info(f'Retrieving the dependencies of {event.package_name}-{event.package_version}')
                    nativeBuildInputs = pythonPackage.get_native_build_inputs()
                    propagatedBuildInputs = pythonPackage.get_propagated_build_inputs()
                    buildInputs = pythonPackage.get_build_inputs()
                    checkInputs = pythonPackage.get_check_inputs()
                    optionalBuildInputs = pythonPackage.get_optional_build_inputs()
                    dependenciesInNixpkgs = []
                    for dep in list(set(nativeBuildInputs) | set(propagatedBuildInputs) | set(buildInputs) | set(checkInputs) | set(optionalBuildInputs)):
                        logging.getLogger('step-by-step').info(f'Processing dependency {dep.name}-{dep.version} of {event.package_name}-{event.package_version}')
                        # check if it's in nixpkgs already
                        if dep.in_nixpkgs():
                            logging.getLogger('step-by-step').info(f'Dependency {dep.name}-{dep.version} of {event.package_name}-{event.package_version} already in nixpkgs')
                            dependenciesInNixpkgs.append(dep)
                        else:
                            depName = dep.name
                            depVersion = dep.version
                            nixPythonPackages = nixPythonPackageRepo.find_by_name(dep.name)
                            nixPythonPackage = next((pkg for pkg in nixPythonPackages if dep.satisfies_spec(pkg.version)), None)
                            if nixPythonPackage:
                                pkg = pythonPackageRepo.find_by_name_and_version(nixPythonPackage.name, nixPythonPackage.version)
                                logging.getLogger('step-by-step').info(f'Found a compatible Python package in Nix for {dep.name}-{dep.version}: {pkg.name}-{pkg.version}')
                                dependenciesInNixpkgs.append(pkg)
                            else:
                                # check if there's a flake for the dependency
                                depFlake = flakeRepo.find_by_name_and_version(depName, depVersion)
                                if depFlake:
                                    logger.debug(f'Flake found for {depName}-{depVersion}')
                                else:
                                    flakeCreated = cls.emit(FlakeRequested(depName, depVersion))
                                    logger.info(f'Flake {dep.name}-{dep.version} created (triggered by "flake {event.package_name}-{event.package_version} requested")')

                    flake = Flake(
                        event.package_name,
                        event.package_version,
                        pythonPackage,
                        cls.cleanup_nixpkgs_dependencies(nativeBuildInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(propagatedBuildInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(buildInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(checkInputs, dependenciesInNixpkgs),
                        cls.cleanup_nixpkgs_dependencies(optionalBuildInputs, dependenciesInNixpkgs))
                    logging.getLogger('step-by-step').info(f'Retrieving recipe for flake {flake.name}-{flake.version}')
                    flakeRecipe = cls.find_recipe_by_flake(flake)
                    if flakeRecipe:
                        logging.getLogger('step-by-step').info(f'Recipe processing')
                        result = flakeRecipe.process()
                    else:
                        logger.critical(f'No recipe available for {event.package_name}-{event.package_version}')

                    if result:
                        logger.info(f'Flake {event.package_name}-{event.package_version} created')
                    else:
                        logger.info(f'Flake {event.package_name}-{event.package_version} could not be created')
            else:
                logger.info(f'Unknown Python package {event.package_name}-{event.package_version}')

        return result

    @classmethod
    def find_recipe_by_flake(cls, flake):
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

    @classmethod
    def cleanup_nixpkgs_dependencies(cls, inputs: List[PythonPackage], inNixpkgs: List[PythonPackage]) -> List[PythonPackage]:
        curatedInputs = list([input for input in inputs if not any((input.name == nixpkg.name) for nixpkg in inNixpkgs)])
        curatedNixpkgs = list([nixpkg for nixpkg in inNixpkgs if any((input.name == nixpkg.name) for input in inputs)])
        return curatedInputs + curatedNixpkgs

    def dependency_in_nixpkgs(self, dep) -> bool:
        return dep.in_nixpkgs() or dep in self.dependencies_in_nixpkgs

    def __str__(self):
        return super(Entity, self).__str__()

    def __eq__(self, other):
        return super(Entity, self).__eq__(other)

    def __hash__(self):
        return super(Entity, self).__hash__()
