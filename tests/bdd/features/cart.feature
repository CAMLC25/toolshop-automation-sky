Feature: Shopping cart
  As a shopper
  I want to add products to my cart
  So that I can review the line totals and cart total

  Background:
    Given I am on the home page

  Scenario Outline: Add product to cart calculates line total and cart total
    When I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I open the cart
    Then the cart contains "<product>"
    And the line price equals the unit price times <quantity>
    And the cart total equals the sum of the line prices

  Examples:
    | product            | quantity |
    | Combination Pliers | 1        |
    | Claw Hammer        | 3        |
