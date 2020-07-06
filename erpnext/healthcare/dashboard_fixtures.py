# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
import json
from frappe import _

def get_data():
	return frappe._dict({
		"dashboards": get_dashboards(),
		"charts": get_charts(),
		"number_cards": get_number_cards(),
	})

def get_company():
	company = frappe.defaults.get_defaults().company
	if company:
		return company
	else:
		company = frappe.get_list("Company", limit=1)
		if company:
			return company[0].name
	return None

def get_dashboards():
	return [{
		"name": "Healthcare",
		"dashboard_name": "Healthcare",
		"charts": [
			{ "chart": "Patient Appointments", "width": "Full"},
			{ "chart": "In-Patient Status", "width": "Half"},
			{ "chart": "Clinical Procedures Status", "width": "Half"},
			{ "chart": "Lab Tests", "width": "Half"},
			{ "chart": "Clinical Procedures", "width": "Half"},
			{ "chart": "Symptoms", "width": "Half"},
			{ "chart": "Diagnoses", "width": "Half"},
			{ "chart": "Department wise Patient Appointments", "width": "Full"}
		],
		"cards": [
			{ "card": "Total Patients" },
			{ "card": "Total Patient Admitted" },
			{ "card": "Open Appointments" },
			{ "card": "Appointments to Bill" }
		]
	}]

def get_charts():
	company = get_company()
	return [
			{
				"doctype": "Dashboard Chart",
				"time_interval": "Daily",
				"name": "Patient Appointments",
				"chart_name": _("Patient Appointments"),
				"timespan": "Last Month",
				"filters_json": json.dumps([
					["Patient Appointment", "company", "=", company, False],
					["Patient Appointment", "status", "!=", "Cancelled"]
				]),
				"chart_type": "Count",
				"timeseries": 1,
				"based_on": "appointment_datetime",
				"owner": "Administrator",
				"document_type": "Patient Appointment",
				"type": "Line",
				"width": "Half"
			},
			{
				"doctype": "Dashboard Chart",
				"name": "Department wise Patient Appointments",
				"chart_name": _("Department wise Patient Appointments"),
				"chart_type": "Custom",
				"source": "Department wise Patient Appointments",
				"filters_json": json.dumps([]),
				'is_public': 1,
				"owner": "Administrator",
				"type": "Bar",
				"width": "Full",
				"custom_options": json.dumps({
					"colors": ["#7CD5FA", "#5F62F6", "#7544E2", "#EE5555"],
					"barOptions":{
						"stacked":1
					},
					"height": 300
				})
			},
			{
				"doctype": "Dashboard Chart",
				"name": "Lab Tests",
				"chart_name": _("Lab Tests"),
				"chart_type": "Group By",
				"document_type": "Lab Test",
				"group_by_type": "Count",
				"group_by_based_on": "template",
				"filters_json": json.dumps([
					["Lab Test", "company", "=", company, False],
					["Lab Test", "docstatus", "=", 1]
				]),
				'is_public': 1,
				"owner": "Administrator",
				"type": "Percentage",
				"width": "Half",
			},
			{
				"doctype": "Dashboard Chart",
				"name": "Clinical Procedures",
				"chart_name": _("Clinical Procedures"),
				"chart_type": "Group By",
				"document_type": "Clinical Procedure",
				"group_by_type": "Count",
				"group_by_based_on": "procedure_template",
				"filters_json": json.dumps([
					["Clinical Procedure", "company", "=", company, False],
					["Clinical Procedure", "docstatus", "=", 1]
				]),
				'is_public': 1,
				"owner": "Administrator",
				"type": "Percentage",
				"width": "Half",
			},
			{
				"doctype": "Dashboard Chart",
				"name": "In-Patient Status",
				"chart_name": _("In-Patient Status"),
				"chart_type": "Group By",
				"document_type": "Inpatient Record",
				"group_by_type": "Count",
				"group_by_based_on": "status",
				"filters_json": json.dumps([
					["Inpatient Record", "company", "=", company, False]
				]),
				'is_public': 1,
				"owner": "Administrator",
				"type": "Bar",
				"width": "Half",
			},
			{
				"doctype": "Dashboard Chart",
				"name": "Clinical Procedures Status",
				"chart_name": _("Clinical Procedure Status"),
				"chart_type": "Group By",
				"document_type": "Clinical Procedure",
				"group_by_type": "Count",
				"group_by_based_on": "status",
				"filters_json": json.dumps([
					["Clinical Procedure", "company", "=", company, False],
					["Clinical Procedure", "docstatus", "=", 1]
				]),
				'is_public': 1,
				"owner": "Administrator",
				"type": "Pie",
				"width": "Half",
			},
			{
				"doctype": "Dashboard Chart",
				"name": "Symptoms",
				"chart_name": _("Symptoms"),
				"chart_type": "Group By",
				"document_type": "Patient Encounter Symptom",
				"group_by_type": "Count",
				"group_by_based_on": "complaint",
				"filters_json": json.dumps([]),
				'is_public': 1,
				"owner": "Administrator",
				"type": "Percentage",
				"width": "Half",
			},
			{
				"doctype": "Dashboard Chart",
				"name": "Diagnoses",
				"chart_name": _("Diagnoses"),
				"chart_type": "Group By",
				"document_type": "Patient Encounter Diagnosis",
				"group_by_type": "Count",
				"group_by_based_on": "diagnosis",
				"filters_json": json.dumps([]),
				'is_public': 1,
				"owner": "Administrator",
				"type": "Percentage",
				"width": "Half",
			}
		]

def get_number_cards():
	company = get_company()
	return [
		{
			"name": "Total Patients",
			"label": _("Total Patients"),
			"function": "Count",
			"doctype": "Number Card",
			"document_type": "Patient",
			"filters_json": json.dumps(
				[["Patient","status","=","Active",False]]
			),
			"is_public": 1,
			"owner": "Administrator",
			"show_percentage_stats": 1,
			"stats_time_interval": "Daily"
		},
		{
			"name": "Total Patients Admitted",
			"label": _("Total Patients Admitted"),
			"function": "Count",
			"doctype": "Number Card",
			"document_type": "Patient",
			"filters_json": json.dumps(
				[["Patient","inpatient_status","=","Admitted",False]]
			),
			"is_public": 1,
			"owner": "Administrator",
			"show_percentage_stats": 1,
			"stats_time_interval": "Daily"
		},
		{
			"name": "Open Appointments",
			"label": _("Open Appointments"),
			"function": "Count",
			"doctype": "Number Card",
			"document_type": "Patient Appointment",
			"filters_json": json.dumps(
				[["Patient Appointment","company","=",company,False],
				["Patient Appointment","status","=","Open",False]]
			),
			"is_public": 1,
			"owner": "Administrator",
			"show_percentage_stats": 1,
			"stats_time_interval": "Daily"
		},
		{
			"name": "Appointments to Bill",
			"label": _("Appointments To Bill"),
			"function": "Count",
			"doctype": "Number Card",
			"document_type": "Patient Appointment",
			"filters_json": json.dumps(
				[["Patient Appointment","company","=",company,False],
				["Patient Appointment","invoiced","=",0,False]]
			),
			"is_public": 1,
			"owner": "Administrator",
			"show_percentage_stats": 1,
			"stats_time_interval": "Daily"
		}
	]