# Automate GenAI evaluation workflows with Microsoft Foundry and GitHub Actions

## Role(s)

- AI Engineer
- Developer
- DevOps Engineer

## Level

Intermediate

## Product(s)

Microsoft Foundry

## Prerequisites

- Completion of "Evaluate GenAI applications manually using Microsoft Foundry" module or equivalent manual evaluation experience
- Familiarity with Python programming and SDK usage
- Basic understanding of GitHub Actions and CI/CD concepts
- Experience with command-line tools and API integration

## Summary

Scale your GenAI evaluation processes through automation using Microsoft Foundry's built-in and custom evaluators. Learn to configure automated evaluation workflows, integrate with CI/CD pipelines using GitHub Actions, and implement comprehensive safety monitoring including red teaming processes. Validate automated systems through shadow rating analysis and optimize evaluation costs while maintaining thorough quality and safety coverage.

## Learning objectives

After completing this module, learners will be able to:

1. **Set up** automated evaluation workflows in Microsoft Foundry using built-in and custom evaluation metrics
2. **Configure** GitHub Actions pipelines to automatically run evaluations and store results in CSV format
3. **Implement** automated risk and safety monitoring systems including red teaming processes for GenAI applications
4. **Analyze** shadow rating results to validate automated evaluation accuracy against human judgment baselines
5. **Optimize** evaluation costs and performance while maintaining comprehensive coverage of quality and safety metrics

## Chunk your content into subtasks

Identify the subtasks of automating GenAI evaluation workflows with Microsoft Foundry and GitHub Actions.

| Subtask | How will you assess it? (Exercise or Knowledge check) | Which learning objective(s) does this help meet? | Does the subtask have enough learning content to justify an entire unit? If not, which other subtask will you combine it with? |
| ---- | ---- | ---- | ---- |
| Configure automated evaluation workflows using Microsoft Foundry SDK | Exercise: Set up and run automated evaluation on test dataset | 1 | Yes - core technical skill requiring detailed SDK implementation |
| Set up GitHub Actions pipeline for automated evaluation | Exercise: Create workflow file and configure automated pipeline | 2 | Yes - requires detailed CI/CD configuration and integration setup |
| Implement automated safety monitoring and red teaming | Exercise: Configure safety evaluators and red teaming agents | 3 | Yes - complex safety processes requiring dedicated coverage |
| Perform shadow rating analysis and validate automated results | Exercise: Compare automated results against manual baselines | 4 | No - combine with cost optimization |
| Optimize evaluation costs and performance | Knowledge check + Exercise: Implement cost-saving strategies and performance tuning | 4, 5 | No - combine with shadow rating analysis |

## Outline the units

Add more units as needed for your content

1. **Introduction**

    Discover how automated evaluation workflows scale manual processes while maintaining quality and safety standards. Learn the role of shadow rating in validating automated systems and understand the integration between Microsoft Foundry evaluators, GitHub Actions, and production deployment pipelines.

2. **Configure automated evaluation workflows using Microsoft Foundry**

    Learn to implement automated evaluation systems using Microsoft Foundry's SDK and built-in evaluators:

    - **Set up Microsoft Foundry evaluation environment**
        - Configure Microsoft Foundry project and authentication for automated access
        - Install and configure the Microsoft Foundry SDK for evaluation workflows
        - Understand built-in evaluator capabilities and limitations
    - **Implement built-in evaluator workflows**
        - Configure groundedness, relevance, coherence, and fluency evaluators
        - Set up batch evaluation processing for large datasets
        - Handle evaluation API responses and error conditions
    - **Develop custom evaluators for specific requirements**
        - Create custom evaluation logic for domain-specific metrics
        - Integrate custom evaluators with Microsoft Foundry evaluation framework
        - Test and validate custom evaluator performance against manual baselines

    **Knowledge check**

    What types of questions will test the learning objective?

    - Code completion: Complete SDK configuration code for evaluation setup
    - Troubleshooting: Identify and resolve common evaluation pipeline errors

3. **Exercise - Build automated evaluation workflow**

    Create a comprehensive automated evaluation system:

    1. Set up Microsoft Foundry project and configure SDK authentication
    2. Implement automated evaluation using built-in evaluators on your test dataset
    3. Create custom evaluator for domain-specific quality metric
    4. Test evaluation workflow and validate results format

4. **Set up GitHub Actions for automated evaluation pipelines**

    Learn to integrate Microsoft Foundry evaluations with CI/CD workflows using GitHub Actions:

    - **Design evaluation pipeline architecture**
        - Plan trigger conditions for evaluation runs (PR creation, scheduled execution)
        - Structure evaluation workflows for different deployment stages
        - Configure secure credential management for Microsoft Foundry access
    - **Create GitHub Actions workflow files**
        - Write YAML configuration for evaluation pipeline execution
        - Configure job dependencies and parallel execution strategies
        - Implement artifact storage and result reporting mechanisms
    - **Integrate with deployment workflows**
        - Set evaluation gates for deployment approval processes
        - Configure failure handling and notification systems
        - Establish rollback procedures based on evaluation results

    **Knowledge check**

    What types of questions will test the learning objective?

    - YAML configuration: Complete GitHub Actions workflow configuration
    - Process design: Sequence evaluation pipeline steps for optimal efficiency

5. **Implement automated safety monitoring and red teaming**

    Configure comprehensive automated safety evaluation using Microsoft Foundry's risk and safety evaluators:

    - **Set up automated content safety evaluation**
        - Configure built-in safety evaluators for harmful content detection
        - Implement custom blocklists and content filtering rules
        - Set up severity thresholds and escalation procedures
    - **Deploy AI red teaming agents**
        - Configure Microsoft Foundry AI red teaming agents for adversarial testing
        - Design automated prompt injection and jailbreak detection
        - Implement systematic vulnerability scanning workflows
    - **Create safety monitoring dashboards**
        - Set up automated safety metric reporting and alerting
        - Configure compliance reporting for regulatory requirements
        - Establish incident response procedures for safety failures

    **Knowledge check**

    What types of questions will test the learning objective?

    - Configuration: Set appropriate safety thresholds for different risk categories
    - Scenario analysis: Design red teaming scenarios for specific GenAI applications

6. **Exercise - Configure comprehensive automated evaluation and safety pipeline**

    Build a complete automated evaluation and safety monitoring system:

    1. Create GitHub Actions workflow combining evaluation and safety monitoring
    2. Configure automated red teaming scans with appropriate scenarios
    3. Set up safety threshold enforcement and failure notifications
    4. Test complete pipeline with sample deployments and safety violations

7. **Validate automated systems through shadow rating and cost optimization**

    Learn to validate automated evaluation accuracy against human baselines and optimize evaluation costs:

    - **Perform shadow rating analysis**
        - Compare automated evaluation results with manual baseline data
        - Calculate correlation metrics and identify systematic biases
        - Calibrate automated evaluators based on human judgment patterns
    - **Optimize evaluation costs and performance**
        - Implement sampling strategies for large-scale evaluation datasets
        - Configure parallel processing and batch optimization
        - Balance evaluation depth with cost constraints and time requirements
    - **Establish continuous improvement workflows**
        - Set up monitoring for evaluation system drift and accuracy degradation
        - Implement feedback loops for continuous evaluator improvement
        - Plan periodic recalibration cycles with updated manual baselines

    **Knowledge check**

    What types of questions will test the learning objective?

    - Statistical analysis: Interpret correlation coefficients between automated and manual evaluations
    - Cost optimization: Select appropriate sampling strategies for different evaluation scenarios

8. **Exercise - Optimize and validate automated evaluation system**

    Complete the automated evaluation system with validation and optimization:

    1. Perform shadow rating analysis comparing your automated results to manual baselines
    2. Implement cost optimization strategies including sampling and parallel processing
    3. Configure monitoring and alerting for evaluation system performance
    4. Document calibration procedures and continuous improvement workflows

9. **Summary**

    Automated evaluation workflows enable scalable quality and safety monitoring for GenAI applications while maintaining the rigor established through manual evaluation processes. You've learned to implement comprehensive automated systems using Microsoft Foundry's built-in and custom evaluators, integrate evaluation pipelines with CI/CD workflows, configure advanced safety monitoring including red teaming, and validate automated systems through shadow rating analysis. These automated capabilities ensure consistent evaluation standards while optimizing costs and enabling rapid deployment cycles with maintained quality assurance.

## Notes

- Exercises should build upon the datasets and baselines created in the manual evaluation module
- Provide template GitHub Actions workflow files and Microsoft Foundry SDK code samples
- Include real examples of shadow rating analysis with interpretation guidance
- Consider cost implications throughout and provide specific optimization strategies
- Red teaming scenarios should be realistic but safe for learning environments
- Emphasize the importance of human oversight even in automated systems