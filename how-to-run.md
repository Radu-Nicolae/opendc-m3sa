# Setup Locally

This page describes steps to build, publish, and run locally OpenDC. In case any setup-related
issues are enocuntered, please view the [Troubleshooting](#troubleshooting) section.

# Requirements

OpenDC requires strict parameters to be run under normal conditions. 
Failing to meet these conditions will most likely result in a failed compilation or compatibility issues.

1. `openjdk 17` or a similar `jdk` environment for **Java 17**
<br>You can check your `jdk` version using:
```bash
java --version
```
2. A shell environment (terminal), able to run `bash` commands. We highly recommend Windows users to run OpenDC under [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).
3. `maven 3.8` or a newer version. Check your `maven` version using:
```bash
mvn --version
```
<br>`maven` is used to handle java libraries, including our built version of OpenDC. `maven` usually comes preinstalled with most IDEs. Otherwise, you can install `maven` as follows:
```bash
# macOS
brew install maven
```
```bash
# Debian based linux distros
sudo apt install maven
```
```bash
# Arch Linux
sudo pacman -S maven
```

<hr>

# Building and publishing as a local java library

### 1. Clone the repository on your device

```bash
git clone https://github.com/atlarge-research/opendc.git
cd opendc/
```

### 2. Initialize the project using `gradle`
``` bash
./gradlew
```
Expected output: **BUILD SUCCESSFUL**.

### 3. Build OpenDC using `gradle`

```bash
./gradlew build
```
The execution should take $\approx 3min, depending on your machine. Expected output: **BUILD SUCCESSFUL**.

### 4. Disable key signing 
i.e., remove GPG artifact signature application in `publishing-conventions.gradle.kts` in order to make publishing to Maven Local possible.

```bash
sed -i  "s/sign(publishing.publications)//g" buildSrc/src/main/kotlin/publishing-conventions.gradle.kts
```

**Note:** This command should not return anything. You can check if this step was processed by running:

```bash
grep -oq "sign(publishing.publications)" buildSrc/src/main/kotlin/publishing-conventions.gradle.kts && echo "Failed" || echo "Successful"
```

### 5. Build and publish OpenDC to `maven` Local as a library

```bash
./gradlew publishToMavenLocal
```

At this point, you should have a built version of OpenDC locally under `~/.m2` that you can use in your personal project.
To check whether these steps were resulted in our expected output, run the following check:

```bash
find ~/.m2/repository/org/opendc/ >/dev/null 2>&1 && echo "Success" || echo "Fail"
```

# Setting up your local project


<hr>

# Troubleshooting 
All these steps were executed on commit [616017b](https://github.com/atlarge-research/opendc/tree/616017ba78a0882fe38b9b171b2b0f68e593cd8d).
We recommend running the steps on the latest commit from the master branch. If any issues are encountered, please report by creating a Github issue, 
and run the steps on [616017b](https://github.com/atlarge-research/opendc/tree/616017ba78a0882fe38b9b171b2b0f68e593cd8d), or search for a more recent,
stable commit. 

```bash
git checkout 616017b
```
