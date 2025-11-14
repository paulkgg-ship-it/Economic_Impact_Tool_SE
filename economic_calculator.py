def calculate_economic_impact(form_data):
    results = {}
    
    total_investment = form_data['total_investment']
    cra_incentive = form_data['cra_incentive']
    private_funding = form_data['private_funding']
    construction_jobs = form_data['construction_jobs']
    construction_avg_wage = form_data['construction_avg_wage']
    permanent_jobs = form_data['permanent_jobs']
    permanent_avg_wage = form_data['permanent_avg_wage']
    construction_duration = form_data['construction_duration']
    analysis_period = form_data['analysis_period']
    annual_operating_costs = form_data['annual_operating_costs']
    annual_revenue = form_data['annual_revenue']
    property_value_increase = form_data['property_value_increase']
    property_tax_rate = form_data['property_tax_rate']
    local_procurement_pct = form_data['local_procurement_pct']
    
    employment_multiplier = form_data['employment_multiplier']
    income_multiplier = form_data['income_multiplier']
    output_multiplier = form_data['output_multiplier']
    sales_tax_rate = form_data['sales_tax_rate']
    
    results['direct_jobs_construction'] = construction_jobs
    indirect_jobs_construction = construction_jobs * (employment_multiplier - 1)
    results['indirect_jobs_construction'] = round(indirect_jobs_construction, 1)
    results['total_jobs_construction'] = round(construction_jobs + indirect_jobs_construction, 1)
    
    results['direct_jobs_permanent'] = permanent_jobs
    indirect_jobs_permanent = permanent_jobs * (employment_multiplier - 1)
    results['indirect_jobs_permanent'] = round(indirect_jobs_permanent, 1)
    results['total_jobs_permanent'] = round(permanent_jobs + indirect_jobs_permanent, 1)
    
    construction_hours = construction_jobs * 2080 * (construction_duration / 12)
    direct_construction_income = construction_hours * construction_avg_wage
    results['direct_construction_income'] = direct_construction_income
    results['total_construction_income'] = direct_construction_income * income_multiplier
    
    permanent_annual_hours = permanent_jobs * 2080
    direct_permanent_income = permanent_annual_hours * permanent_avg_wage
    results['direct_permanent_income_annual'] = direct_permanent_income
    results['total_permanent_income_annual'] = direct_permanent_income * income_multiplier
    results['total_permanent_income_period'] = results['total_permanent_income_annual'] * analysis_period
    
    results['direct_output'] = total_investment
    results['total_output'] = total_investment * output_multiplier
    results['indirect_induced_output'] = results['total_output'] - results['direct_output']
    
    annual_property_tax = property_value_increase * (property_tax_rate / 100)
    results['annual_property_tax'] = annual_property_tax
    results['total_property_tax_period'] = annual_property_tax * analysis_period
    
    local_spending = (annual_operating_costs + annual_revenue) * (local_procurement_pct / 100)
    annual_sales_tax = local_spending * (sales_tax_rate / 100)
    results['annual_sales_tax'] = annual_sales_tax
    results['total_sales_tax_period'] = annual_sales_tax * analysis_period
    
    results['total_tax_revenue_period'] = results['total_property_tax_period'] + results['total_sales_tax_period']
    results['annual_tax_revenue'] = results['annual_property_tax'] + results['annual_sales_tax']
    
    if cra_incentive > 0:
        results['roi_ratio'] = results['total_tax_revenue_period'] / cra_incentive
        results['payback_years'] = cra_incentive / results['annual_tax_revenue'] if results['annual_tax_revenue'] > 0 else 0
    else:
        results['roi_ratio'] = 0
        results['payback_years'] = 0
    
    results['leverage_ratio'] = private_funding / cra_incentive if cra_incentive > 0 else 0
    
    results['total_income_all_sources'] = results['total_construction_income'] + results['total_permanent_income_period']
    
    results['community_benefits'] = {
        'affordable_housing_units': form_data['affordable_housing_units'],
        'public_space_sqft': form_data['public_space_sqft'],
        'parking_spaces': form_data['parking_spaces'],
        'retail_units': form_data['retail_units']
    }
    
    return results
