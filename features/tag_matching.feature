@fixture.tag.management
Feature: Verify tag inclusion based on Geo Targeting and Minutely Budget

        Scenario: Geo Targeting passes for a tag with no geo targeting
            Given tags exist with
                  | name   | minutely_budget | allowed_countries |
                  | no_geo |                 |                   |
             When a request to debug is made with "country=USA"
             Then tag "no_geo" should be "INCLUDED" in the debug response considered tags

        Scenario: Geo Targeting passes for a tag with geo targeting where request is in allowedCountries list
            Given tags exist with
                  | name    | minutely_budget | allowed_countries |
                  | USA_geo |                 | USA               |
             When a request to debug is made with "country=USA"
             Then tag "USA_geo" should be "INCLUDED" in the debug response considered tags

        Scenario: Geo Targeting passes for a tag with multiple geo targeting and request is in allowedCountries list
            Given tags exist with
                  | name      | minutely_budget | allowed_countries |
                  | multi_geo |                 | USA,CAN           |
             When a request to debug is made with "country=USA"
             Then tag "multi_geo" should be "INCLUDED" in the debug response considered tags

        @clear.all.tags
        Scenario: Geo targeting fails for a tag with geo targeting where request is not in allowedCountries list
            Given tags exist with
                  | name    | minutely_budget | allowed_countries |
                  | USA_geo |                 | USA               |
             When a request to debug is made with "country=CAN"
             Then tag "USA_geo" should be "BLOCKED: COUNTRY" in the debug response considered tags
              And the debug response should have no bid

        Scenario: Budget targeting passes when budget is defined and not exceeded
            Given tags exist with
                  | name    | minutely_budget | allowed_countries |
                  | budget1 | 1               |                   |
             When a request to debug is made with "country=USA"
             Then tag "budget1" should be "INCLUDED" in the debug response considered tags

        @clear.all.tags
        Scenario: Budget targeting fails when budget is defined and exceeded
            Given tags exist with
                  | name    | minutely_budget | allowed_countries |
                  | budget1 | 1               |                   |
             When a request to debug is made with "country=USA"
              And the tags impression pixel is requested
              And the tags impression pixel is requested again
              And a request to debug is made with "country=USA"
             Then tag "budget1" should be "BLOCKED: BUDGET" in the debug response considered tags
              And the debug response should have no bid
