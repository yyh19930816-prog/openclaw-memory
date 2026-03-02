#!/usr/bin/env python3
"""
GitHub Actions Runner Operator - Python Implementation
Source: https://github.com/evryfs/github-actions-runner-operator
Date: 2023-04-01
Description: K8s operator for scheduling GitHub Actions runner pods
"""

import os
import logging
from kubernetes import client, config
from kubernetes.client import V1Pod, V1ObjectMeta, V1PodSpec, V1Container


class GitHubActionsRunnerOperator:
    def __init__(self, namespace="default"):
        """Initialize operator with Kubernetes client and configuration"""
        config.load_incluster_config()  # For running inside cluster
        self.api = client.CoreV1Api()
        self.namespace = namespace
        self.logger = logging.getLogger(__name__)
        
        # GitHub App credentials from environment
        self.app_id = os.getenv("GITHUB_APP_ID")
        self.private_key = os.getenv("GITHUB_PRIVATE_KEY")
        
    def _create_runner_pod(self, runner_name: str, repo_url: str, token: str):
        """Create a Kubernetes pod for GitHub Actions runner"""
        pod = V1Pod(
            metadata=V1ObjectMeta(
                name=f"github-runner-{runner_name}",
                labels={"app": "github-runner"}
            ),
            spec=V1PodSpec(
                containers=[
                    V1Container(
                        name="runner",
                        image="myoung34/github-runner:latest",
                        env=[
                            {"name": "RUNNER_NAME", "value": runner_name},
                            {"name": "REPO_URL", "value": repo_url},
                            {"name": "ACCESS_TOKEN", "value": token},
                        ],
                        resources={
                            "requests": {"cpu": "500m", "memory": "512Mi"},
                            "limits": {"cpu": "1000m", "memory": "1Gi"}
                        }
                    )
                ],
                restart_policy="Never"
            )
        )
        return self.api.create_namespaced_pod(namespace=self.namespace, body=pod)
    
    def schedule_runner(self, runner_name: str, repo_url: str):
        """Main method to schedule a new runner pod"""
        try:
            # In production, get runner registration token from GitHub API
            # For demo, we use a placeholder token
            registration_token = "ghp_exampletoken123"  
            
            self.logger.info(f"Scheduling runner {runner_name} for {repo_url}")
            pod = self._create_runner_pod(runner_name, repo_url, registration_token)
            self.logger.info(f"Created pod {pod.metadata.name}")
            return pod
        except Exception as e:
            self.logger.error(f"Failed to schedule runner: {e}")
            raise

    def cleanup(self):
        """Clean up completed runner pods"""
        try:
            pods = self.api.list_namespaced_pod(
                namespace=self.namespace,
                label_selector="app=github-runner"
            )
            
            for pod in pods.items:
                if pod.status.phase == "Succeeded" or pod.status.phase == "Failed":
                    self.logger.info(f"Cleaning up pod {pod.metadata.name}")
                    self.api.delete_namespaced_pod(
                        name=pod.metadata.name,
                        namespace=self.namespace
                    )
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Example usage of the operator"""
    logging.basicConfig(level=logging.INFO)
    operator = GitHubActionsRunnerOperator()
    
    # Schedule a runner
    operator.schedule_runner(
        runner_name="test-runner-1",
        repo_url="https://github.com/evryfs/github-actions-runner-operator"
    )
    
    # Perform cleanup of completed pods
    operator.cleanup()


if __name__ == "__main__":
    main()