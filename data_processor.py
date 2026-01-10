from typing import Dict, Any


class DataProcessor:
    """
    Hard-coded economic multipliers for multiple geographies
    Supports Homestead CRA and Florida Statewide
    """

    def __init__(self):
        # ===== HOMESTEAD CRA DATA =====
        # Hard-coded multipliers from Lightcast data for Homestead
        self.multipliers_by_industry = {
            'cafe': {
                'naics_code': '722515',
                'industry_name': 'Snack and Nonalcoholic Beverage Bars',
                'output_multiplier': 1.52,
                'employment_multiplier': 1.34,
                'earnings_multiplier': 1.41,
                'indirect_multiplier': 0.32,
                'induced_multiplier': 0.20
            },
            'restaurant': {
                'naics_code': '722511',
                'industry_name': 'Full-Service Restaurants',
                'output_multiplier': 1.58,
                'employment_multiplier': 1.38,
                'earnings_multiplier': 1.45,
                'indirect_multiplier': 0.35,
                'induced_multiplier': 0.23
            },
            'retail': {
                'naics_code': '452000',
                'industry_name': 'General Merchandise Stores',
                'output_multiplier': 1.45,
                'employment_multiplier': 1.28,
                'earnings_multiplier': 1.35,
                'indirect_multiplier': 0.28,
                'induced_multiplier': 0.17
            },
            'office': {
                'naics_code': '531120',
                'industry_name': 'Lessors of Nonresidential Buildings',
                'output_multiplier': 1.62,
                'employment_multiplier': 1.42,
                'earnings_multiplier': 1.55,
                'indirect_multiplier': 0.38,
                'induced_multiplier': 0.24
            },
            'bar': {
                'naics_code': '722410',
                'industry_name': 'Drinking Places (Alcoholic Beverages)',
                'output_multiplier': 1.55,
                'employment_multiplier': 1.36,
                'earnings_multiplier': 1.43,
                'indirect_multiplier': 0.33,
                'induced_multiplier': 0.22
            },
            'brewery': {
                'naics_code': '312120',
                'industry_name': 'Breweries',
                'output_multiplier': 1.68,
                'employment_multiplier': 1.45,
                'earnings_multiplier': 1.58,
                'indirect_multiplier': 0.42,
                'induced_multiplier': 0.26
            },
            'distillery': {
                'naics_code': '312140',
                'industry_name': 'Distilleries',
                'output_multiplier': 1.72,
                'employment_multiplier': 1.48,
                'earnings_multiplier': 1.62,
                'indirect_multiplier': 0.44,
                'induced_multiplier': 0.28
            }
        }

        # Homestead demographics from Esri
        self.homestead_demographics = {
            'population': 80378,
            'median_income': 45230,
            'labor_force': 35420,
            'unemployment_rate': 0.045,
            'median_age': 35.2
        }
        
        # Alias for backwards compatibility
        self.demographics = self.homestead_demographics

        # Homestead real estate data from CoStar
        self.real_estate_by_type = {
            'retail': {
                'avg_rent_psf': 24.50,
                'occupancy_rate': 0.92,
                'cap_rate': 0.072,
                'market_rent': 22.80
            },
            'restaurant': {
                'avg_rent_psf': 26.00,
                'occupancy_rate': 0.90,
                'cap_rate': 0.075,
                'market_rent': 24.50
            },
            'office': {
                'avg_rent_psf': 22.00,
                'occupancy_rate': 0.88,
                'cap_rate': 0.068,
                'market_rent': 20.50
            }
        }
        
        # Homestead fiscal parameters
        self.homestead_fiscal_parameters = {
            'city_millage': 5.9604,
            'county_millage': 4.574,
            'combined_millage': 10.5340,
            'cra_capture_rate': 0.95,
            'hard_cost_capitalization_rate': 0.60,
            'property_value_annual_growth': 0.03,
            'note': 'FY 2025 millage rates for City of Homestead and Miami-Dade County'
        }

        # ===== FLORIDA STATEWIDE DATA =====
        # Florida statewide multipliers (higher due to larger economy)
        self.florida_statewide_multipliers = {
            'cafe': {
                'naics_code': '722515',
                'industry_name': 'Snack and Nonalcoholic Beverage Bars',
                'output_multiplier': 1.48,
                'employment_multiplier': 1.30,
                'earnings_multiplier': 1.38,
                'indirect_multiplier': 0.30,
                'induced_multiplier': 0.18
            },
            'restaurant': {
                'naics_code': '722511',
                'industry_name': 'Full-Service Restaurants',
                'output_multiplier': 1.55,
                'employment_multiplier': 1.35,
                'earnings_multiplier': 1.42,
                'indirect_multiplier': 0.33,
                'induced_multiplier': 0.22
            },
            'retail': {
                'naics_code': '452000',
                'industry_name': 'General Merchandise Stores',
                'output_multiplier': 1.42,
                'employment_multiplier': 1.25,
                'earnings_multiplier': 1.32,
                'indirect_multiplier': 0.26,
                'induced_multiplier': 0.16
            },
            'office': {
                'naics_code': '531120',
                'industry_name': 'Lessors of Nonresidential Buildings',
                'output_multiplier': 1.58,
                'employment_multiplier': 1.38,
                'earnings_multiplier': 1.50,
                'indirect_multiplier': 0.35,
                'induced_multiplier': 0.23
            },
            'bar': {
                'naics_code': '722410',
                'industry_name': 'Drinking Places (Alcoholic Beverages)',
                'output_multiplier': 1.52,
                'employment_multiplier': 1.33,
                'earnings_multiplier': 1.40,
                'indirect_multiplier': 0.31,
                'induced_multiplier': 0.21
            },
            'brewery': {
                'naics_code': '312120',
                'industry_name': 'Breweries',
                'output_multiplier': 1.65,
                'employment_multiplier': 1.42,
                'earnings_multiplier': 1.55,
                'indirect_multiplier': 0.40,
                'induced_multiplier': 0.25
            },
            'distillery': {
                'naics_code': '312140',
                'industry_name': 'Distilleries',
                'output_multiplier': 1.70,
                'employment_multiplier': 1.45,
                'earnings_multiplier': 1.60,
                'indirect_multiplier': 0.42,
                'induced_multiplier': 0.28
            }
        }

        # Florida statewide demographics
        self.florida_statewide_demographics = {
            'population': 22_610_726,
            'median_income': 63_062,
            'labor_force': 10_800_000,
            'unemployment_rate': 0.032,
            'median_age': 42.5
        }

        # Florida statewide real estate (average across state)
        self.florida_statewide_real_estate = {
            'retail': {
                'avg_rent_psf': 28.50,
                'occupancy_rate': 0.94,
                'cap_rate': 0.065,
                'market_rent': 27.00
            },
            'restaurant': {
                'avg_rent_psf': 30.00,
                'occupancy_rate': 0.92,
                'cap_rate': 0.070,
                'market_rent': 28.50
            },
            'office': {
                'avg_rent_psf': 32.00,
                'occupancy_rate': 0.90,
                'cap_rate': 0.062,
                'market_rent': 30.00
            }
        }

        # Florida statewide fiscal parameters (requires local input)
        self.florida_statewide_fiscal_parameters = {
            'city_millage': 0.0,
            'county_millage': 0.0,
            'combined_millage': 0.0,
            'cra_capture_rate': 0.0,
            'hard_cost_capitalization_rate': 0.60,
            'property_value_annual_growth': 0.03,
            'note': 'Florida statewide - fiscal parameters require local jurisdiction input. Economic impacts (jobs, output) are calculated; fiscal impacts are not applicable without local millage rates.'
        }

    def get_relevant_multipliers(self, industry_type: str, geography: str = "homestead") -> Dict[str, Any]:
        """
        Get multipliers for the specific industry type and geography
        """
        industry = industry_type.lower().strip()
        
        # Select multiplier set based on geography
        if geography == "florida_statewide":
            multiplier_set = self.florida_statewide_multipliers
        else:
            multiplier_set = self.multipliers_by_industry

        # Try exact match first
        if industry in multiplier_set:
            return multiplier_set[industry]

        # Try partial matches
        for key in multiplier_set.keys():
            if key in industry or industry in key:
                return multiplier_set[key]

        # Default to restaurant if not found
        print(f"Warning: Industry '{industry_type}' not found, defaulting to restaurant")
        return multiplier_set['restaurant']

    def get_demographics(self, geography: str = "homestead") -> Dict[str, Any]:
        """Get demographic data for the specified geography"""
        if geography == "florida_statewide":
            return self.florida_statewide_demographics
        return self.homestead_demographics

    def get_real_estate_data(self, property_type: str, geography: str = "homestead") -> Dict[str, Any]:
        """Get real estate metrics for property type and geography"""
        prop_type = property_type.lower().strip()
        
        if geography == "florida_statewide":
            real_estate_set = self.florida_statewide_real_estate
        else:
            real_estate_set = self.real_estate_by_type

        if prop_type in real_estate_set:
            return real_estate_set[prop_type]

        return real_estate_set['retail']

    def get_fiscal_parameters(self, geography: str = "homestead") -> Dict[str, Any]:
        """Get fiscal parameters for the specified geography"""
        if geography == "florida_statewide":
            return self.florida_statewide_fiscal_parameters
        return self.homestead_fiscal_parameters

    def prepare_llm_context(self, form_data: Dict[str, Any], geography: str = "homestead") -> Dict[str, Any]:
        """
        Main function: Prepare condensed context for LLM

        Args:
            form_data: All the form inputs from the user
            geography: Either "homestead" or "florida_statewide"

        Returns:
            Condensed context with only relevant data
        """
        # Determine industry from proposed use
        proposed_use = form_data.get('proposed_use', 'restaurant')

        # Determine property type (for real estate data)
        property_type_map = {
            'cafe': 'restaurant',
            'coffee': 'restaurant',
            'restaurant': 'restaurant',
            'bar': 'restaurant',
            'brewery': 'restaurant',
            'distillery': 'restaurant',
            'retail': 'retail',
            'store': 'retail',
            'shop': 'retail',
            'office': 'office',
            'coworking': 'office'
        }

        property_type = 'retail'
        for key, ptype in property_type_map.items():
            if key in proposed_use.lower():
                property_type = ptype
                break

        # Get relevant data for the selected geography
        multipliers = self.get_relevant_multipliers(proposed_use, geography)
        demographics = self.get_demographics(geography)
        real_estate = self.get_real_estate_data(property_type, geography)
        fiscal_params = self.get_fiscal_parameters(geography)

        # Determine source labels based on geography
        if geography == "florida_statewide":
            multiplier_source = 'Lightcast 2025 data for Florida statewide'
            demo_source = 'US Census 2024 data for Florida'
            real_estate_source = 'CoStar 2025 Florida statewide averages'
        else:
            multiplier_source = 'Lightcast 2025 data for Homestead/South Dade region'
            demo_source = 'Esri 2025 demographics for Homestead, FL'
            real_estate_source = 'CoStar 2025 data for Homestead retail/restaurant market'

        # Build condensed context
        context = {
            'geography': geography,
            'geography_display': 'Florida Statewide' if geography == 'florida_statewide' else 'Homestead CRA',
            'project_inputs': form_data,
            'economic_multipliers': {
                'naics_code': multipliers['naics_code'],
                'industry_name': multipliers['industry_name'],
                'output_multiplier': multipliers['output_multiplier'],
                'employment_multiplier': multipliers['employment_multiplier'],
                'earnings_multiplier': multipliers['earnings_multiplier'],
                'indirect_multiplier': multipliers['indirect_multiplier'],
                'induced_multiplier': multipliers['induced_multiplier'],
                'note': multiplier_source
            },
            'demographics': {
                'population': demographics['population'],
                'median_income': demographics['median_income'],
                'labor_force': demographics['labor_force'],
                'unemployment_rate': demographics['unemployment_rate'],
                'source': demo_source
            },
            'real_estate': {
                'avg_rent_psf': real_estate['avg_rent_psf'],
                'occupancy_rate': real_estate['occupancy_rate'],
                'cap_rate': real_estate['cap_rate'],
                'market_rent': real_estate['market_rent'],
                'property_type': property_type,
                'source': real_estate_source
            },
            'fiscal_parameters': fiscal_params
        }

        return context


# Create singleton instance
data_processor = DataProcessor()
