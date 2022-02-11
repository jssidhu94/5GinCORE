"""
Simple example custom service, used to drive shell commands on a node.
"""
from typing import Tuple

from core.nodes.base import CoreNode
from core.services.coreservices import CoreService, ServiceMode


class ExampleService(CoreService):
    """
    Example Custom CORE Service
    :cvar name: name used as a unique ID for this service and is required, no spaces
    :cvar group: allows you to group services within the GUI under a common name
    :cvar executables: executables this service depends on to function, if executable is
        not on the path, service will not be loaded
    :cvar dependencies: services that this service depends on for startup, tuple of
        service names
    :cvar dirs: directories that this service will create within a node
    :cvar configs: files that this service will generate, without a full path this file
        goes in the node's directory e.g. /tmp/pycore.12345/n1.conf/myfile
    :cvar startup: commands used to start this service, any non-zero exit code will
        cause a failure
    :cvar validate: commands used to validate that a service was started, any non-zero
        exit code will cause a failure
    :cvar validation_mode: validation mode, used to determine startup success.
        NON_BLOCKING    - runs startup commands, and validates success with validation commands
        BLOCKING        - runs startup commands, and validates success with the startup commands themselves
        TIMER           - runs startup commands, and validates success by waiting for "validation_timer" alone
    :cvar validation_timer: time in seconds for a service to wait for validation, before
        determining success in TIMER/NON_BLOCKING modes.
    :cvar validation_period: period in seconds to wait before retrying validation,
        only used in NON_BLOCKING mode
    :cvar shutdown: shutdown commands to stop this service
    """

    name: str = "Docker-Test"
    group: str = "Utility"
    executables: Tuple[str, ...] = ()
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/var/lib/docker/containers/", "/run/shm", "/run/resolvconf")
    configs: Tuple[str, ...] = ("myservice1.sh", "myservice2.sh")
    startup: Tuple[str, ...] = tuple(f"sh {x}" for x in configs)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.
        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.
        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.
        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = "#!/bin/sh\n"
        if filename == cls.configs[0]:
            # Docker likes to think it has DNS set up or it complains.
            # Unless your network was attached to the Internet this is
            # non-functional but hides error messages.
            cfg += 'echo "nameserver 8.8.8.8" > /run/resolvconf/resolv.conf\n'
            #
            # Make sure the docker service uses the directory structure we are about to create
            cfg += 'echo DOCKER_OPTS=\\"--dns 8.8.8.8 --exec-opt native.cgroupdriver=cgroupfs -g $PWD/docker\\" > /etc/default/docker\n'
            # Docker does not like links so must do a mount --bind
            cfg += 'mkdir -p docker/overlay2 \n'
            cfg += 'mount -o bind /var/lib/docker/overlay2/ docker/overlay2/\n'
            # We want our own container directory though so we do not pollute the host
            cfg += 'mkdir mymnt \n'
            cfg += 'mount -o bind mymnt/ docker/overlay2/mnt/\n'
            # We need to know where the images are so we link symbolically
            cfg += 'ln -s /var/lib/docker/image/ docker/image\n'
            #
            cfg += 'CGROUP=/sys/fs/cgroup\n'
            cfg += 'mount -n -t tmpfs -o uid=0,gid=0,mode=0755 cgroup $CGROUP\n'
            cfg += 'for SUBSYS in $(cut -d: -f2 /proc/1/cgroup)\n'
            cfg += 'do\n'
            cfg += '        mkdir $CGROUP/$SUBSYS\n'
            cfg += '        mountpoint -q $CGROUP/$SUBSYS\n'
            cfg += '        mount -n -t cgroup -o $SUBSYS cgroup $CGROUP/$SUBSYS\n'
            cfg += '        echo $SUBSYS | grep -q ^name= && {\n'
            cfg += '                NAME=$(echo $SUBSYS | sed s/^name=//)\n'
            cfg += '                ln -s $SUBSYS $CGROUP/$NAME\n'
            cfg += '        }\n'
            cfg += '        [ $SUBSYS = cpuacct,cpu ] && ln -s $SUBSYS $CGROUP/cpu,cpuacct\n'
            cfg += 'done\n'
            #
            # Starts the docker service. In Ubuntu this is docker.io; in other
            # distros may just be docker
            cfg += 'service docker start\n'

        elif filename == cls.configs[1]:
            cfg += "echo hello"
        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.
        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.
        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate