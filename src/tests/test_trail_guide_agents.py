#!/usr/bin/env python3
"""
Trail Guide Agent Test Suite
Adventure Works Outdoor Gear - AI Trail Assistant Testing

Comprehensive test suite for all versions of the Trail Guide Agent.
Version: 1.0.0
Created: 2026-01-16
"""

import os
import sys
import json
import pytest
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()


class TrailGuideAgentTestSuite:
    """Comprehensive test suite for Trail Guide agents."""
    
    def __init__(self, project_endpoint: str):
        """
        Initialize the test suite.
        
        Args:
            project_endpoint: Azure AI Projects endpoint URL
        """
        self.project_endpoint = project_endpoint
        self.client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential()
        )
        
        # Test scenarios by category
        self.test_scenarios = {
            "basic_functionality": [
                {
                    "id": "basic_001",
                    "query": "What gear do I need for a day hike?",
                    "expected_keywords": ["backpack", "water", "hiking"],
                    "max_response_time": 5.0
                },
                {
                    "id": "basic_002", 
                    "query": "Recommend a trail for beginners",
                    "expected_keywords": ["beginner", "easy", "trail"],
                    "max_response_time": 5.0
                }
            ],
            "safety_guidance": [
                {
                    "id": "safety_001",
                    "query": "What safety precautions for solo hiking?",
                    "expected_keywords": ["safety", "emergency", "plan"],
                    "max_response_time": 10.0
                },
                {
                    "id": "safety_002",
                    "query": "How to handle bear encounters?",
                    "expected_keywords": ["bear", "safety", "avoid"],
                    "max_response_time": 10.0
                }
            ],
            "gear_recommendations": [
                {
                    "id": "gear_001",
                    "query": "Best Adventure Works gear for winter hiking?",
                    "expected_keywords": ["adventure works", "winter", "gear"],
                    "max_response_time": 8.0
                },
                {
                    "id": "gear_002",
                    "query": "Backpacking gear list for 3 days",
                    "expected_keywords": ["backpack", "tent", "sleeping"],
                    "max_response_time": 8.0
                }
            ],
            "location_specific": [
                {
                    "id": "location_001",
                    "query": "Best trails near Seattle for families",
                    "expected_keywords": ["seattle", "family", "trail"],
                    "max_response_time": 10.0
                },
                {
                    "id": "location_002",
                    "query": "Mount Rainier hiking conditions",
                    "expected_keywords": ["mount rainier", "conditions", "hiking"],
                    "max_response_time": 12.0
                }
            ]
        }
    
    def run_functional_tests(self, agent_id: str, agent_version: str) -> Dict[str, Any]:
        """
        Run functional tests on a specific agent.
        
        Args:
            agent_id: ID of the agent to test
            agent_version: Version identifier (e.g., "v1", "v2", "v3")
            
        Returns:
            dict: Test results
        """
        print(f"🧪 Running functional tests for {agent_version} agent...")
        
        results = {
            "agent_id": agent_id,
            "agent_version": agent_version,
            "test_timestamp": datetime.now().isoformat(),
            "categories": {},
            "summary": {}
        }
        
        total_tests = 0
        total_passed = 0
        
        for category, scenarios in self.test_scenarios.items():
            print(f"   Testing category: {category}")
            
            category_results = {
                "scenarios": [],
                "passed": 0,
                "failed": 0,
                "avg_response_time": 0
            }
            
            response_times = []
            
            for scenario in scenarios:
                test_result = self._run_single_test(agent_id, scenario)
                category_results["scenarios"].append(test_result)
                
                if test_result["status"] == "passed":
                    category_results["passed"] += 1
                    total_passed += 1
                    if "response_time" in test_result:
                        response_times.append(test_result["response_time"])
                else:
                    category_results["failed"] += 1
                
                total_tests += 1
                print(f"     {scenario['id']}: {test_result['status']}")
            
            if response_times:
                category_results["avg_response_time"] = sum(response_times) / len(response_times)
            
            results["categories"][category] = category_results
        
        # Calculate summary metrics
        results["summary"] = {
            "total_tests": total_tests,
            "tests_passed": total_passed,
            "tests_failed": total_tests - total_passed,
            "success_rate": total_passed / total_tests if total_tests > 0 else 0,
            "overall_avg_response_time": sum(
                cat["avg_response_time"] for cat in results["categories"].values() 
                if cat["avg_response_time"] > 0
            ) / len([cat for cat in results["categories"].values() if cat["avg_response_time"] > 0])
        }
        
        return results
    
    def _run_single_test(self, agent_id: str, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single test scenario.
        
        Args:
            agent_id: ID of the agent to test
            scenario: Test scenario definition
            
        Returns:
            dict: Single test result
        """
        try:
            start_time = datetime.now()
            
            response = self.client.agents.invoke(
                agent_id=agent_id,
                messages=[{"role": "user", "content": scenario["query"]}]
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            # Validate response
            validation_results = self._validate_response(response.content, scenario)
            
            return {
                "scenario_id": scenario["id"],
                "query": scenario["query"],
                "response": response.content,
                "response_time": response_time,
                "validations": validation_results,
                "status": "passed" if validation_results["all_passed"] else "failed",
                "timestamp": start_time.isoformat()
            }
            
        except Exception as e:
            return {
                "scenario_id": scenario["id"],
                "query": scenario["query"],
                "error": str(e),
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_response(self, response: str, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate agent response against scenario expectations.
        
        Args:
            response: Agent response text
            scenario: Test scenario with validation criteria
            
        Returns:
            dict: Validation results
        """
        validations = {
            "keyword_checks": [],
            "response_length_ok": len(response) > 50,  # Minimum meaningful response
            "all_passed": True
        }
        
        response_lower = response.lower()
        
        # Check for expected keywords
        for keyword in scenario.get("expected_keywords", []):
            found = keyword.lower() in response_lower
            validations["keyword_checks"].append({
                "keyword": keyword,
                "found": found
            })
            if not found:
                validations["all_passed"] = False
        
        # Check response quality indicators
        quality_indicators = [
            "helpful", "adventure works", "trail", "hiking", 
            "safety", "gear", "recommend"
        ]
        
        quality_score = sum(1 for indicator in quality_indicators if indicator in response_lower)
        validations["quality_score"] = quality_score / len(quality_indicators)
        
        if validations["quality_score"] < 0.2:  # Less than 20% quality indicators
            validations["all_passed"] = False
        
        if not validations["response_length_ok"]:
            validations["all_passed"] = False
        
        return validations
    
    def run_performance_tests(self, agent_id: str, agent_version: str) -> Dict[str, Any]:
        """
        Run performance tests on an agent.
        
        Args:
            agent_id: ID of the agent to test
            agent_version: Version identifier
            
        Returns:
            dict: Performance test results
        """
        print(f"⚡ Running performance tests for {agent_version} agent...")
        
        # Performance test scenarios
        performance_scenarios = [
            {"query": "Quick trail recommendation", "expected_max_time": 3.0},
            {"query": "Detailed gear list for backpacking with explanations and safety tips", "expected_max_time": 8.0},
            {"query": "Complex multi-part question: What trails near Portland are good for families with children under 10, what gear do we need, what are the safety considerations, and what's the weather forecast?", "expected_max_time": 15.0}
        ]
        
        results = {
            "agent_id": agent_id,
            "agent_version": agent_version,
            "test_timestamp": datetime.now().isoformat(),
            "performance_tests": [],
            "summary": {}
        }
        
        response_times = []
        performance_passed = 0
        
        for i, scenario in enumerate(performance_scenarios, 1):
            try:
                print(f"   Performance test {i}/{len(performance_scenarios)}")
                
                start_time = datetime.now()
                response = self.client.agents.invoke(
                    agent_id=agent_id,
                    messages=[{"role": "user", "content": scenario["query"]}]
                )
                end_time = datetime.now()
                
                response_time = (end_time - start_time).total_seconds()
                response_times.append(response_time)
                
                performance_met = response_time <= scenario["expected_max_time"]
                if performance_met:
                    performance_passed += 1
                
                results["performance_tests"].append({
                    "scenario": scenario["query"],
                    "response_time": response_time,
                    "expected_max_time": scenario["expected_max_time"],
                    "performance_met": performance_met,
                    "response_length": len(response.content)
                })
                
            except Exception as e:
                results["performance_tests"].append({
                    "scenario": scenario["query"],
                    "error": str(e),
                    "performance_met": False
                })
        
        # Calculate performance summary
        results["summary"] = {
            "total_performance_tests": len(performance_scenarios),
            "performance_tests_passed": performance_passed,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "performance_score": performance_passed / len(performance_scenarios)
        }
        
        return results
    
    def run_regression_tests(self, agent_ids: Dict[str, str]) -> Dict[str, Any]:
        """
        Run regression tests comparing multiple agent versions.
        
        Args:
            agent_ids: Dictionary mapping version names to agent IDs
            
        Returns:
            dict: Regression test results
        """
        print(f"🔄 Running regression tests across agent versions...")
        
        regression_query = "I'm a beginner hiker planning my first overnight trip. What do I need to know about gear, trail selection, and safety?"
        
        results = {
            "regression_query": regression_query,
            "test_timestamp": datetime.now().isoformat(),
            "version_results": {},
            "comparison": {}
        }
        
        # Test each version
        for version, agent_id in agent_ids.items():
            try:
                print(f"   Testing {version}...")
                
                start_time = datetime.now()
                response = self.client.agents.invoke(
                    agent_id=agent_id,
                    messages=[{"role": "user", "content": regression_query}]
                )
                end_time = datetime.now()
                
                results["version_results"][version] = {
                    "agent_id": agent_id,
                    "response": response.content,
                    "response_time": (end_time - start_time).total_seconds(),
                    "word_count": len(response.content.split()),
                    "contains_gear_advice": "gear" in response.content.lower(),
                    "contains_safety_advice": "safety" in response.content.lower(),
                    "mentions_adventure_works": "adventure works" in response.content.lower()
                }
                
            except Exception as e:
                results["version_results"][version] = {
                    "agent_id": agent_id,
                    "error": str(e),
                    "status": "failed"
                }
        
        # Generate comparison insights
        successful_versions = [v for v in results["version_results"].values() if "error" not in v]
        
        if len(successful_versions) > 1:
            results["comparison"] = {
                "response_times": {v: r["response_time"] for v, r in results["version_results"].items() if "response_time" in r},
                "word_counts": {v: r["word_count"] for v, r in results["version_results"].items() if "word_count" in r},
                "feature_coverage": {
                    "gear_advice_coverage": sum(1 for r in successful_versions if r["contains_gear_advice"]),
                    "safety_advice_coverage": sum(1 for r in successful_versions if r["contains_safety_advice"]),
                    "brand_integration": sum(1 for r in successful_versions if r["mentions_adventure_works"])
                }
            }
        
        return results
    
    def generate_test_report(self, test_results: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive test report.
        
        Args:
            test_results: List of test result dictionaries
            
        Returns:
            str: Formatted test report
        """
        report_lines = [
            "# Trail Guide Agent Test Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary"
        ]
        
        for result in test_results:
            if "summary" in result:
                agent_version = result.get("agent_version", "Unknown")
                summary = result["summary"]
                
                report_lines.extend([
                    f"### {agent_version.upper()} Agent",
                    f"- Tests Run: {summary.get('total_tests', 'N/A')}",
                    f"- Success Rate: {summary.get('success_rate', 0):.1%}",
                    f"- Avg Response Time: {summary.get('overall_avg_response_time', 0):.2f}s",
                    ""
                ])
        
        return "\n".join(report_lines)
    
    def save_results(self, results: Dict[str, Any], test_type: str, agent_version: str = None):
        """Save test results to file."""
        os.makedirs("test_results", exist_ok=True)
        
        if agent_version:
            filename = f"test_results/{test_type}-{agent_version}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        else:
            filename = f"test_results/{test_type}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 {test_type.title()} results saved to: {filename}")


def main():
    """Main test execution function."""
    print("🧪 Trail Guide Agent Test Suite")
    print("=" * 50)
    
    # Load configuration
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    
    if not project_endpoint:
        print("❌ PROJECT_ENDPOINT environment variable is required")
        return 1
    
    # Load agent IDs
    agent_ids = {
        "v1": os.getenv("V1_AGENT_ID"),
        "v2": os.getenv("V2_AGENT_ID"), 
        "v3": os.getenv("V3_AGENT_ID")
    }
    
    available_agents = {k: v for k, v in agent_ids.items() if v}
    
    if not available_agents:
        print("❌ No agent IDs found. Set V1_AGENT_ID, V2_AGENT_ID, or V3_AGENT_ID environment variables.")
        return 1
    
    print(f"🎯 Testing agents: {', '.join(available_agents.keys())}")
    
    # Initialize test suite
    test_suite = TrailGuideAgentTestSuite(project_endpoint)
    
    all_results = []
    
    try:
        # Run functional tests for each agent
        for version, agent_id in available_agents.items():
            print(f"\n{'='*20} Testing {version.upper()} Agent {'='*20}")
            
            # Functional tests
            functional_results = test_suite.run_functional_tests(agent_id, version)
            test_suite.save_results(functional_results, "functional", version)
            all_results.append(functional_results)
            
            # Performance tests
            performance_results = test_suite.run_performance_tests(agent_id, version)
            test_suite.save_results(performance_results, "performance", version)
        
        # Run regression tests if multiple agents available
        if len(available_agents) > 1:
            print(f"\n{'='*20} Regression Tests {'='*20}")
            regression_results = test_suite.run_regression_tests(available_agents)
            test_suite.save_results(regression_results, "regression")
        
        # Generate final report
        report = test_suite.generate_test_report(all_results)
        with open(f"test_results/test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md", "w") as f:
            f.write(report)
        
        print(f"\n✅ Test suite completed successfully!")
        print(f"📊 Results saved to test_results/ directory")
        
        return 0
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())