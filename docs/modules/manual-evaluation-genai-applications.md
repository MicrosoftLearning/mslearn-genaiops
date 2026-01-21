# Evaluate GenAI applications manually using Microsoft Foundry

## Role(s)

- AI Engineer
- Developer
- Data Scientist

## Level

Intermediate

## Product(s)

Microsoft Foundry

## Prerequisites

- Familiarity with generative AI concepts and applications
- Basic understanding of machine learning model evaluation principles
- Basic GitHub repository management skills
- Experience working with CSV files and data formats

## Summary

Learn to systematically evaluate generative AI applications through manual testing processes. Create structured test datasets, apply quality assessment criteria, and establish baseline evaluation standards for GenAI outputs. Implement collaborative evaluation workflows using GitHub for version control and result tracking, while building foundation skills for shadow rating validation of automated evaluation systems.

## Learning objectives

After completing this module, learners will be able to:

1. **Create** structured test datasets and data mapping schemas for comprehensive GenAI model evaluation
2. **Evaluate** GenAI application outputs manually using quality metrics including groundedness, relevance, coherence, and fluency
3. **Configure** manual safety testing processes to identify harmful content and potential risks in GenAI applications
4. **Implement** GitHub-based workflows to store, version, and collaborate on manual evaluation results using CSV format
5. **Establish** baseline human judgment patterns for shadow rating comparison with automated systems

## Chunk your content into subtasks

Identify the subtasks of evaluating GenAI applications manually using Microsoft Foundry.

| Subtask | How will you assess it? (Exercise or Knowledge check) | Which learning objective(s) does this help meet? | Does the subtask have enough learning content to justify an entire unit? If not, which other subtask will you combine it with? |
| ---- | ---- | ---- | ---- |
| Design test dataset structure and create evaluation schema | Exercise: Create CSV template and sample test data | 1 | Yes - foundational to all other activities |
| Perform manual quality assessment using standardized metrics | Exercise: Evaluate sample GenAI outputs using rubrics | 2 | Yes - core skill requiring detailed explanation and practice |
| Conduct safety evaluation and identify harmful content | Knowledge check + Exercise: Safety evaluation checklist and sample content review | 3 | Yes - critical safety skill with specific procedures |
| Set up GitHub repository and implement evaluation workflows | Exercise: Create repo, commit evaluation results, collaborate via PR | 4 | No - combine with establishing baseline patterns |
| Establish baseline patterns and prepare for shadow rating | Exercise: Analyze evaluation consistency and document judgment criteria | 4, 5 | No - combine with GitHub workflows |

## Outline the units

Add more units as needed for your content

1. **Introduction**

    Learn why manual evaluation is essential for GenAI applications and how it establishes the foundation for trustworthy AI systems. Understand the relationship between manual evaluation, automated systems, and the shadow rating approach for validation.

2. **Create structured test datasets for GenAI evaluation**

    Learn to design comprehensive test datasets and evaluation schemas for GenAI applications:

    - **Design evaluation data structure**
        - Define CSV schema for test inputs, expected outputs, and evaluation criteria
        - Map evaluation fields to quality and safety metrics
        - Structure metadata for tracking evaluation context and versioning
    - **Create representative test datasets**
        - Select diverse, representative test cases for your GenAI application domain
        - Balance positive and negative test scenarios
        - Include edge cases and boundary conditions
    - **Establish data quality standards**
        - Define consistency criteria for test data creation
        - Document test case selection rationale and coverage goals
        - Plan for dataset versioning and maintenance

    **Knowledge check**

    What types of questions will test the learning objective?

    - Multiple choice: Which CSV fields are essential for tracking evaluation metadata?
    - Scenario-based: Given a GenAI application, select appropriate test cases for evaluation dataset

3. **Exercise - Build your evaluation dataset**

    Create a comprehensive test dataset for a sample GenAI application:

    1. Design a CSV schema with required evaluation fields
    2. Create 10-15 diverse test cases covering different scenarios
    3. Document your test case selection criteria and coverage strategy
    4. Validate dataset structure for consistency and completeness

4. **Perform manual quality assessment using standardized metrics**

    Learn systematic approaches to manually evaluating GenAI outputs using industry-standard quality metrics:

    - **Apply groundedness evaluation**
        - Assess whether responses are based on provided context or reliable sources
        - Use structured rubrics to rate factual accuracy and source attribution
        - Document evidence and reasoning for groundedness judgments
    - **Evaluate relevance and coherence**
        - Rate response relevance to user queries using standardized scales
        - Assess logical flow, consistency, and coherence of generated content
        - Apply inter-rater reliability techniques for consistent evaluation
    - **Assess fluency and quality**
        - Evaluate language quality, grammar, and natural expression
        - Rate overall response helpfulness and completeness
        - Balance technical accuracy with user experience considerations

    **Knowledge check**

    What types of questions will test the learning objective?

    - Practical application: Rate sample GenAI outputs using provided rubrics
    - True/false: Statements about quality metric application and scoring criteria

5. **Configure manual safety testing and risk assessment**

    Implement systematic safety evaluation processes to identify potential harms and risks in GenAI applications:

    - **Identify harmful content categories**
        - Apply Microsoft Foundry safety categories (hate, sexual, violence, self-harm)
        - Recognize bias, fairness issues, and discriminatory content
        - Detect potential privacy violations and sensitive information exposure
    - **Conduct manual red teaming**
        - Design adversarial prompts to test system boundaries
        - Document prompt injection attempts and jailbreak scenarios  
        - Evaluate system responses to harmful or inappropriate requests
    - **Document safety assessment results**
        - Create safety evaluation reports with severity classifications
        - Track safety issues and mitigation requirements
        - Establish escalation procedures for critical safety findings

    **Knowledge check**

    What types of questions will test the learning objective?

    - Classification: Categorize sample content according to safety risk levels
    - Scenario analysis: Identify potential safety issues in given GenAI interactions

6. **Exercise - Conduct comprehensive manual evaluation**

    Perform systematic manual evaluation on your test dataset:

    1. Apply quality assessment rubrics to evaluate all test cases
    2. Conduct safety evaluation and document any identified risks
    3. Calculate inter-rater reliability scores if working in teams
    4. Create evaluation summary report with findings and recommendations

7. **Implement collaborative evaluation workflows with GitHub**

    Establish version-controlled evaluation workflows using GitHub for team collaboration and result tracking:

    - **Set up evaluation repository structure**
        - Create organized folder structure for datasets, results, and documentation
        - Implement CSV file naming conventions and metadata standards
        - Configure repository settings for collaboration and access control
    - **Establish evaluation workflow processes**
        - Create evaluation guidelines and documentation for team consistency
        - Implement pull request workflows for evaluation result review
        - Document inter-rater reliability procedures and conflict resolution
    - **Prepare baseline data for shadow rating**
        - Analyze evaluation consistency and identify judgment patterns
        - Create baseline datasets for automated system validation
        - Document human evaluation criteria for automated system calibration

    **Knowledge check**

    What types of questions will test the learning objective?

    - Process understanding: Sequence the steps in a collaborative evaluation workflow
    - Tool application: Identify appropriate GitHub features for evaluation result management

8. **Exercise - Establish evaluation workflow and baseline patterns**

    Create a complete collaborative evaluation workflow:

    1. Set up GitHub repository with proper structure and documentation
    2. Commit your evaluation results and create pull request for review
    3. Analyze evaluation consistency and document baseline patterns
    4. Create shadow rating preparation documentation for future automated validation

9. **Summary**

    Manual evaluation forms the foundation of trustworthy GenAI applications by establishing human judgment baselines, identifying potential risks, and creating structured processes for quality assessment. You've learned to create comprehensive test datasets, apply systematic evaluation criteria, implement safety testing procedures, and establish collaborative workflows that prepare your organization for scaling evaluation through automation while maintaining human oversight and validation capabilities.

## Notes

- Exercises should use a consistent sample GenAI application (e.g., customer service chatbot, content generation tool) throughout the module for coherent learning experience
- Provide evaluation rubric templates and example CSV schemas as downloadable resources
- Include real examples of safety issues and appropriate responses for context
- Consider providing a template GitHub repository that learners can fork for the exercises
- Shadow rating concepts should be introduced but not deeply explored (save detailed coverage for Module 2)