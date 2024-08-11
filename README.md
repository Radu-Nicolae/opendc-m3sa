<a href="https://opendc.org/">
    <img src="https://opendc.org/img/logo.png" alt="OpenDC logo" title="OpenDC" align="right" height="100" />
</a>


# OpenDC

Collaborative Datacenter Simulation and Exploration for Everybody

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](/LICENSE.txt)
[![Documentation](https://img.shields.io/badge/docs-master-green.svg)](https://atlarge-research.github.io/opendc)
[![GitHub release](https://img.shields.io/github/v/release/atlarge-research/opendc?include_prereleases)](https://github.com/atlarge-research/opendc/releases)
[![Build](https://github.com/atlarge-research/opendc/actions/workflows/build.yml/badge.svg)](https://github.com/atlarge-research/opendc/actions/workflows/build.yml)

-----

## Docker Steps

#### 1. Build the docker image
```shell
docker build -t m3sa-experiments .
```

#### 2. Run the container
```shell
docker run -d --name m3sa-experiments-container m3sa-experiments
```

#### 3.1 Run hello_world
```shell
docker exec -it m3sa-experiments-container python3 hello_world.py
```

#### 3.2 Access the container
```shell
docker exec -it m3sa-experiments-container /bin/bash
```

#### 3.3 Move test.txt outside the container, inside this folder
```shell
docker cp m3sa-experiments-container:opendc/hello-world.txt ./experiments-output
```

#### 4. Run scenario.cli
```shell
docker exec -it m3sa-experiments-container java -cp 'opendc-experiments-base.jar:lib/*' org.opendc.experiments.base.runner.ScenarioCli --scenario-path "/opendc/experiments/use-case-scenario/inputs/scenario-energy-usage-1-model.json" -p 4 -a
```

#### Last Step. Remove the container and the image
```shell
docker rm -f m3sa-experiments-container && docker rmi m3sa-experiments && docker builder prune -f && clear
```


This repository is the home of the OpenDC project, a free and open-source platform for cloud datacenter simulation.

## Latest Release

- General Availability (GA): [OpenDC v2.0](https://github.com/atlarge-research/opendc/releases/tag/v2.0) (May 10, 2021)
- Preview (Release Candidate): [OpenDC v3.0-rc1](https://github.com/atlarge-research/opendc/releases/tag/v3.0-rc1) (Jan 27, 2023)

## Documentation

You can find the OpenDC documentation [on the website](https://atlarge-research.github.io/opendc/).
The documentation is divided into several sections:

* [Getting Started](https://atlarge-research.github.io/opendc/docs/category/getting-started/)
* [Tutorials](https://atlarge-research.github.io/opendc/docs/category/tutorials/)
* [Advanced Guides](https://atlarge-research.github.io/opendc/docs/category/advanced-guides/)
* [Where to Get Support](https://atlarge-research.github.io/opendc/community/support/)
* [Contributing Guide](https://atlarge-research.github.io/opendc/community/contributing/)

The source code for the documentation is located in [site](site).

## Contributing

Questions, suggestions and contributions are welcome and appreciated!
Please refer to the [contributing guidelines](CONTRIBUTING.md) for more details.

## License

OpenDC is distributed under the MIT license. See [LICENSE.txt](/LICENSE.txt).
