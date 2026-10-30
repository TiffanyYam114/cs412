# File: voter_analytics/views.py
# Author: Tiffany Yam (tiffyam@bu.edu), 10/29/26
# Description: Contains views for the voter_analytics app.

from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Voter

# Import plotly library for graphing
import plotly
import plotly.graph_objs as go

# Create your views here.

class VoterListView(ListView):
    """View to display Voter information."""

    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """Get the results from a query on the Voter objects."""

        results = super().get_queryset()

        # Look for URL parameters to filter by
        if "party_affiliation" in self.request.GET:
            party_affiliation = self.request.GET["party_affiliation"]
            results = results.filter(party_affiliation=party_affiliation)
        if "min_dob_year" in self.request.GET:
            min_dob_year = self.request.GET["min_dob_year"]
            results = results.filter(date_of_birth__gte=f"{min_dob_year}-01-01")
        if "max_dob_year" in self.request.GET:
            max_dob_year = self.request.GET["max_dob_year"]
            results = results.filter(date_of_birth__lte=f"{max_dob_year}-01-01")
        if "v20state" in self.request.GET:
            results = results.filter(v20state=True)
        if "v21town" in self.request.GET:
            results = results.filter(v21town=True)
        if "v21primary" in self.request.GET:
            results = results.filter(v21primary=True)
        if "v22general" in self.request.GET:
            results = results.filter(v22general=True)
        if "v23town" in self.request.GET:
            results = results.filter(v23town=True)
        if "voter_score" in self.request.GET:
            voter_score = self.request.GET["voter_score"]
            results = results.filter(voter_score=voter_score)

        return results

    def get_context_data(self, **kwargs):
        """Return the context dictionary for use in the template."""

        context = super().get_context_data(**kwargs)
        party_affiliations = ['U ', 'D ', 'R ', 'J ', 'A ', 'CC', 'X ', 
        'L ', 'Q ', 'S ', 'FF', 'G ', 'HH', 'T ', 'AA', 'GG', 'Z ', 'O ', 
        'P ', 'E ', 'V ', 'H ', 'Y ', 'W ', 'EE', 'K ']
        previous_elections = ["v20state", "v21town", "v21primary", "v22general", "v23town"]

        context["queries"] = self.request.GET
        context["party_affiliations"] = [party for party in party_affiliations]
        context["years"] = [str(year) for year in range(1920, 2005)]
        context["previous_elections"] = [election for election in previous_elections]
        context["voter_scores"] = [str(score) for score in range(6)]
        
        return context


class VoterDetailView(DetailView):
    """View to display information for a single Voter."""

    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "v"


class GraphsListView(VoterListView):
    """View to display graphs of data about Voters."""

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"
    paginate_by = None

    def get_context_data(self, **kwargs):
        """Return the context dictionary for use in the template."""

        context = super().get_context_data(**kwargs)

        # Get the data for all voters
        voters = context["voters"]

        ##################### Year of Birth Graph ######################
        # Count the number of voters born in each year
        year_count = {}
        for voter in voters:
            year = str(voter.date_of_birth)[:4]
            if year not in year_count:
                year_count[year] = 1
            else:
                year_count[year] += 1

        x = sorted(year_count)
        y = [year_count[year] for year in x]

        # Create a bar chart that shows distribution of voters by year of birth
        fig = go.Bar(x=x, y=y)
        title_text = "Voter Distribution by Year of Birth"
        graph_yob_distribution = plotly.offline.plot({"data": [fig], "layout_title_text": title_text}, 
                                                       auto_open=False, output_type="div")
        context["graph_yob_distribution"] = graph_yob_distribution


        ##################### Party Affiliation Graph ######################
        # Count the number of voters in each party
        party_count = {}
        for voter in voters:
            party = voter.party_affiliation
            if party not in party_count:
                party_count[party] = 1
            else:
                party_count[party] += 1

        labels = [party for party in party_count]
        values = [party_count[party] for party in party_count]

        # Create a pie chart that shows distribution of voters by party affiliation
        fig = go.Pie(labels=labels, values=values)
        title_text = "Voter Distribution by Party Affiliation"
        graph_party_distribution = plotly.offline.plot({"data": [fig], "layout_title_text": title_text}, 
                                                       auto_open=False, output_type="div")
        context["graph_party_distribution"] = graph_party_distribution


        ##################### Election Participation Graph ######################
        # Count the number of voters who voted in each election
        election_count = {
            "v20state": 0,
            "v21town": 0, 
            "v21primary": 0, 
            "v22general": 0, 
            "v23town": 0, 
        }
        for voter in voters:
            if voter.v20state == True:
                election_count["v20state"] += 1
            if voter.v21town == True:
                election_count["v21town"] += 1
            if voter.v21primary == True:
                election_count["v21primary"] += 1
            if voter.v22general == True:
                election_count["v22general"] += 1
            if voter.v23town == True:
                election_count["v23town"] += 1

        x = [election for election in election_count]
        y = [election_count[election] for election in election_count]

        # Create a bar chart that shows distribution of voters by election participation
        fig = go.Bar(x=x, y=y)
        title_text = "Voter Distribution by Election Participation"
        graph_election_distribution = plotly.offline.plot({"data": [fig], "layout_title_text": title_text}, 
                                                        auto_open=False, output_type="div")
        context["graph_election_distribution"] = graph_election_distribution


        return context