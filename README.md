<h1 align="center">
  <br>
  Data Api Gateway Env Component
</h1>

[![Generic badge](https://img.shields.io/badge/python-3.9.0-darkgreen.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/nodejs-16.13.0-purple.svg)](https://shields.io/)

---

# Requirements

1. [Docker](https://www.docker.com/) >= 20.10.10
2. [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

---

## Context

A Data Api Gateway plugin is a set of subcomponents that create an environment capable of receiving, validating and sending data following a single data model. This plugin has the following features:

- Domain Router
- API Gateway
- Schema Validator
- Single Data Model

# How to use

1. Edit your manifest file (example in [template/manifest.yaml](template/manifest.yaml))

   ```yaml
   api_gateway:
     region: us-east-1 # ------------- (string) --- [REQUIRED]
     name: gw_name # ----------------- (string) --- [REQUIRED]
     type: PRIVATE # ----------------- (string) --- [REQUIRED]
     auth:
       iam_auth: TRUE # -------------- (boolean) -- [REQUIRED]
       api_key: TRUE # --------------- (boolean) -- [REQUIRED]
     registry: registry_name # ------- (string) --- [REQUIRED]
     record: # ------------------------------------ [OPTIONAL]
       zone_id: YOUR_HOSTED_ZONE_ID
     vpc_endpoint: # ------------------------------ [REQUIRED] for PRIVATE API-GW
       vpc_id: # --------------------- (string)
       subnets_ids: # ---------------- (list of subnet ids)
         - subnet-first_subnet
         - subnet-second_subnet
         - subnet-third_subnet
       security_group:
         ip_blocks_sg: # ------------- (list of Ingress CIDR IP blocks)
           - 10.0.0.0/21
         eg_blocks_sg: # ------------- (list of Egress CIDR IP blocks)
           - 0.0.0.0/0
   ```

2. Have your AWS credentials available to run the component. Credentials can be used via environment variables, or also via credentials stored locally in a file (usually in `~/.aws/credentials`). Credentials can be acquired in the following ways:

   a. Using the command `aws sso login` (Must [configure SSO](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) on the machine);

   b. Exporting environment variables or _profile_. You must go to the AWS SSO Start URL and select the desired account. Then select the `Command line or programmatic access` option. In the displayed tab, choose according to your operating system, copy and paste the credentials as environment variables (`Option 1: Set AWS environment variables`) or for the profile in the local credentials file (`Option 2: Add a profile to your AWS credentials file`, typically in `~/.aws/credentials`).

3. Build the Docker image using the command:

```docker
docker build -t data-api-gateway-component:latest .
```

4. Run the component application using the following Docker command:

```docker
docker run \
-v $PWD/template:/src/template \
-v ~/.aws:/home/orange/.aws \
-i data-api-gateway-component:latest \
apply data-api-gateway -f /src/template/manifest.yaml
```

In this example the volumes passed maps the component manifest file, and the AWS configuration and credentials directory.

Credentials can be used in container execution by being passed in environment variables:

```docker
docker run \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
-e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
-v $PWD/template:/src/template \
-i data-api-gateway-component:latest \
apply data-api-gateway -f /src/template/manifest.yaml
```

# For developers

## Requirements

1. Python >= 3.9.0
2. NodeJS >= 16.13.0
3. [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

Run these commands in sequence, at the root of the project:

1. Create a python virtual environment based on the version passed through the "-p" parameter:

```sh
python3 -m venv venv
```

2. Activate the virtual environment:

```sh
source venv/bin/activate
```

3. Install project dependencies and make commands executable:

```sh
pip3 install -r ./requirements.txt --disable-pip-version-check && pip3 install --editable .
```

or

```sh
python setup.py install
```

4. Define the PYTHONPATH

```sh
export PYTHONPATH=$PWD
```

5. Edit your manifest file and set your AWS Credentials (see section **How To use**, items 1 and 2)

6. Apply your configuration using following command of this component:

```sh
data-api-gateway apply data-api-gateway -f template/manifest.yaml
```

Observations:

1. If you want to deactivate the virtual environment, use:

   deactivate

2. If you want to clean-up python cache and distribution files and bundled virtual environment libraries use:

```sh
   find . -type d -name "\_\_pycache\_\_" -exec rm -rf {} + && \
   rm -rf \*\*/\_.egg-info && \
   rm -rf .mypy_cache/ venv/ build/ dist/ && rm -rf .tox
```

---

# Unit Tests and Coverage

For test execution, **pytest** (framework used for creating tests in a dynamic and fast way) is used together with **tox** (used for automation and standardization testing in Python). Your tests should be developed in python, which makes the code smaller, more readable and easier to maintain.

To run the specified test suites, run the `tox` command at the root of the repository.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
