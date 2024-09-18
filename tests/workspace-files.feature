# Tests for the presence of the expected workflow files

Feature: Workspace files

    As a researcher,
    I want to make sure that my workflow produces expected files,
    so that I can be sure that the workflow outputs are correct.

    Scenario: The workspace contains the expected input files
        When the workflow is finished
        Then the workspace should include "analysis.py"

    Scenario: The workflow generates the final plot
        When the workflow is finished
        Then the workspace should contain "histogram.png"
        And the sha256 checksum of the file "histogram.png" should be "c8f87114530c049d587f355cef07280fa5d760910c32638136a713eab1aa72e1"
        And all the outputs should be included in the workspace