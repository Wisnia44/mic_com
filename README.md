# MIC COM

## Comparison between different composition of microservices

Developed as support material for master thesis.

Compares mocks of two different compositions based on orchestration and choreography patterns.

## Development

### Start project locally

Project contains two separate projects actually. To run one of them you have to go into its directory. Please use `cd choreography` or `cd orchestration`.\
After that simply run `docker-compose up`.\
The environment will be ready after `pipenv install` command.

### Using pre-commit

To use pre-commit you need to run 2 commands: `pip install pre-commit` and `pre-commit install`.\
It may be needed to authorize with the passphrase for the SSH key to Github.

## Modelling

### Services list

0. Orchestrator - optional;
1. AI;
2. CRM;
3. Doors;
4. E-receipt;
5. Messages;
6. Payments;
7. PIM;
8. Receipt;
9. Screen;
10. Terminal.

### Databases list

1. CRM's database;
2. PIM's database.

CRM keeps in the database information about customers, PIM does so regarding products.\
The rest of the services are just controllers (including the orchestrator) and they don't need the databases.
