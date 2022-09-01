.PHONY: help build deploy test clean

INFRA_DIR	:= ./infra/
TEST_DIR 	:= ./tests/

help: ## shows Makefile commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## builds the Lambda function using AWS SAM
	cd ${INFRA_DIR} && \
	sam build

deploy: build ## deploys the stack using AWS SAM
	cd ${INFRA_DIR} && \
	sam deploy --guided --capabilities CAPABILITY_NAMED_IAM

test:  ## runs tests
	pytest ${TEST_DIR}

clean: ## cleans artifacts
	rm -rf infra/.aws-sam
	rm infra/samconfig.toml
