#!/usr/bin/env python
"""Stacker module for creating a Bitbucket Pipelines user."""
from __future__ import print_function

from collections import OrderedDict

from troposphere import (
    And, Equals, If, Join, Not, NoValue, Output, Ref, Region, Select, iam
)

import awacs.iam
from awacs.aws import Allow, Statement, Policy

from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import CFNCommaDelimitedList, CFNString


class User(Blueprint):
    """Extends Stacker Blueprint class."""

    VARIABLES = {
        'ManagedPolicies': {'type': CFNCommaDelimitedList,
                            'description': '(Optional) List of managed '
                                           'policies to associate with the '
                                           'user.',
                            'default': ''},
        'CustomerName': {'type': CFNString,
                         'description': '(Optional) The nickname for the '
                                        'customer. Must be all lowercase '
                                        'letters, should not contain spaces '
                                        'or special characters, nor should it '
                                        'include any part of EnvironmentName.',
                         'allowed_pattern': '[-_ a-z]*',
                         'default': ''},
        'EnvironmentName': {'type': CFNString,
                            'description': 'Name of Environment',
                            'default': 'common'},
        'UserName': {'type': CFNString,
                     'description': '(Optional) Manually specify user name '
                                    '(leave blank to generate from '
                                    'EnvironmentName & CustomerName).',
                     'default': ''}
    }

    def create_template(self):
        """Create template (main function called by Stacker)."""
        template = self.template
        variables = self.get_variables()
        template.add_version('2010-09-09')
        template.add_description("Bitbucket Pipeline User v1.0.0")

        # Conditions
        usernamespecified = 'UserNameSpecified'
        template.add_condition(
            usernamespecified,
            And(Not(Equals(variables['UserName'].ref, '')),
                Not(Equals(variables['UserName'].ref, 'undefined')))
        )
        managedpoliciesspecified = 'ManagedPoliciesSpecified'
        template.add_condition(
            managedpoliciesspecified,
            And(Not(Equals(Select(0, variables['ManagedPolicies'].ref),
                           '')),
                Not(Equals(Select(0, variables['ManagedPolicies'].ref),
                           'undefined')))
        )

        # Resources
        def deduped_permissions():
            """Return list of IAM permissions for resource *."""
            actions_to_dedupe = [
                # Manage updates to this template and managed policies
                awacs.iam.CreatePolicyVersion,
                awacs.iam.DeletePolicyVersion,
                awacs.iam.PutUserPolicy
            ]
            # Order preserving dedupe adapted from:
            # https://stackoverflow.com/a/17016257
            return list(OrderedDict.fromkeys(actions_to_dedupe))

        bitbucketuser = template.add_resource(
            iam.User(
                'BitbucketUser',
                ManagedPolicyArns=If(
                    managedpoliciesspecified,
                    variables['ManagedPolicies'].ref,
                    NoValue
                ),
                Policies=[
                    iam.Policy(
                        PolicyName='BitbucketUserPolicy',
                        PolicyDocument=Policy(
                            Version='2012-10-17',
                            Statement=[
                                Statement(
                                    Action=deduped_permissions(),
                                    Effect=Allow,
                                    Resource=['*']
                                ),
                                # Statement(
                                #     Action=[awacs.iam.GetUser],
                                #     Effect=Allow,
                                #     Resource=[
                                #         Join('-',
                                #              ['REPLACEME'])
                                #
                                #     ]
                                # )
                            ]
                        )
                    )
                ],
                UserName=If(
                    usernamespecified,
                    variables['UserName'].ref,
                    Join('-', ['Bitbucket',
                               variables['CustomerName'].ref,
                               variables['EnvironmentName'].ref,
                               Region])
                )
            )
        )
        template.add_output(
            Output(
                'UserName',
                Description='IAM user name',
                Value=Ref(bitbucketuser)
            )
        )


# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context
    print(User('test', Context({"namespace": "test"}), None).to_json())
