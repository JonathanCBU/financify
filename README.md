# financify
A set of accessible python functions for managing massive financial spreadsheets

## Release Process

1. Create the release branch
    - Checkout the commit you want to base your release off of
    - Create a branch of the format `release/vMAJ.MIN.PATCH`, updating the appropriate section
2. Change the version number
    - Update the version number in `pyproject.toml`
    - Update the version number in `CHANGELOG.md` and add a new `Unreleased` section
    - Commit the version number changes
3. Push the release branch and create a PR
    - Push the release branch to the remote
    - Create a PR from the release branch to `main`
    - Add the `release` label to the PR
4. After the PR is merged, finalize the drafted release
    - Open the drafted release and change the target to "main"
    - Publish the release

## Wash Sale Detector

### Context

- When a security is sold at a loss, and then that same security is purchased within 30 days of the loss sale
- A short term wash sale loss is defined as a loss from a wash sale of an asset that was held for under 365 calendar days
- A long term wash sale loss is defined as a loss from a wash sale of an asset that was held for 365 calendar days or more
- [Here is an investor.gov](https://www.investor.gov/introduction-investing/investing-basics/glossary/wash-sales#:~:text=A%20wash%20sale%20occurs%20when,to%20buy%20substantially%20identical%20securities) article that defines a wash sale

### Requirements

- wash_sale_detector should report the sum of all wash sale losses
- wash_sale_detector should report itemized wash sale losses
- wash_sale_detector should report short and long term wash sale losses
- wash_sale_detector should be able to parse data sets with more information than necessary for wash sale loss calculation
- wash_sale_detector should produce an output/report file rather than just printing results