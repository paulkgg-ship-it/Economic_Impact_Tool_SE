from typing import Dict, Any


class DataProcessor:
    """
    Hard-coded economic multipliers for Homestead CRA (MVP version)
    Later we'll load these from actual data files
    """

    def __init__(self):
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

        # Hard-coded Homestead demographics from Esri
        self.demographics = {
            'population': 80378,
            'median_income': 45230,
            'labor_force': 35420,
            'unemployment_rate': 0.045,
            'median_age': 35.2
        }

        # Hard-coded real estate data from CoStar for Homestead
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

    def get_relevant_multipliers(self, industry_type: str) -> Dict[str, Any]:
        """
        Get multipliers for the specific industry type

        Args:
            industry_type: e.g., "cafe", "restaurant", "retail"

        Returns:
            Dictionary with relevant multipliers
        """
        # Clean up the industry type
        industry = industry_type.lower().strip()

        # Try exact match first
        if industry in self.multipliers_by_industry:
            return self.multipliers_by_industry[industry]

        # Try partial matches
        for key in self.multipliers_by_industry.keys():
            if key in industry or industry in key:
                return self.multipliers_by_industry[key]

        # Default to restaurant if not found
        print(
            f"Warning: Industry '{industry_type}' not found, defaulting to restaurant"
        )
        return self.multipliers_by_industry['restaurant']

    def get_demographics(self) -> Dict[str, Any]:
        """Get Homestead demographic data"""
        return self.demographics

    def get_real_estate_data(self, property_type: str) -> Dict[str, Any]:
        """
        Get real estate metrics for property type

        Args:
            property_type: "retail", "restaurant", or "office"

        Returns:
            Dictionary with real estate metrics
        """
        prop_type = property_type.lower().strip()

        if prop_type in self.real_estate_by_type:
            return self.real_estate_by_type[prop_type]

        # Default to retail
        return self.real_estate_by_type['retail']

    def prepare_llm_context(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main function: Prepare condensed context for LLM

        This reduces 3.2M cells to ~100 lines of JSON

        Args:
            form_data: All the form inputs from the user

        Returns:
            Condensed context with only relevant data
        """
        # Determine industry from proposed use
        proposed_use = form_data.get('proposed_use', 'restaurant')

        # Determine property type (for real estate data)
        # Map common uses to property types
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

        property_type = 'retail'  # default
        for key, ptype in property_type_map.items():
            if key in proposed_use.lower():
                property_type = ptype
                break

        # Get relevant multipliers
        multipliers = self.get_relevant_multipliers(proposed_use)

        # Build condensed context
        context = {
            'project_inputs': form_data,
            'economic_multipliers': {
                'naics_code':
                multipliers['naics_code'],
                'industry_name':
                multipliers['industry_name'],
                'output_multiplier':
                multipliers['output_multiplier'],
                'employment_multiplier':
                multipliers['employment_multiplier'],
                'earnings_multiplier':
                multipliers['earnings_multiplier'],
                'indirect_multiplier':
                multipliers['indirect_multiplier'],
                'induced_multiplier':
                multipliers['induced_multiplier'],
                'note':
                'Multipliers from Lightcast 2025 data for Homestead/South Dade region'
            },
            'demographics': {
                'population': self.demographics['population'],
                'median_income': self.demographics['median_income'],
                'labor_force': self.demographics['labor_force'],
                'unemployment_rate': self.demographics['unemployment_rate'],
                'source': 'Esri 2025 demographics for Homestead, FL'
            },
            'real_estate': {
                'avg_rent_psf':
                self.get_real_estate_data(property_type)['avg_rent_psf'],
                'occupancy_rate':
                self.get_real_estate_data(property_type)['occupancy_rate'],
                'cap_rate':
                self.get_real_estate_data(property_type)['cap_rate'],
                'market_rent':
                self.get_real_estate_data(property_type)['market_rent'],
                'property_type':
                property_type,
                'source':
                'CoStar 2025 data for Homestead retail/restaurant market'
            },
            'fiscal_parameters': {
                'city_millage':
                5.9604,
                'county_millage':
                4.574,
                'combined_millage':
                10.5340,
                'cra_capture_rate':
                0.95,
                'hard_cost_capitalization_rate':
                0.60,
                'property_value_annual_growth':
                0.03,
                'note':
                'FY 2025 millage rates for City of Homestead and Miami-Dade County'
            }
        }

        return context


# Create singleton instance
data_processor = DataProcessor()
