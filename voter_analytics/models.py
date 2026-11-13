# File: voter_analytics.models.py
# Author: Tiffany Yam (tiffyam@bu.edu), 10/29/26
# Description: Contains data models for the voter_analytics app.

from django.db import models

# Create your models here.

class Voter(models.Model):
    """Models the data attributes of a voter."""

    # Identification
    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()

    # Address
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()

    # Dates
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    # Voter status
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.IntegerField()

    # Voting history
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a string representation of this Voter."""
        return (f"{self.first_name} {self.last_name} - {self.zip_code} - {self.party_affiliation} - {self.voter_score}"
                f"{self.v20state} {self.v21town} {self.v21primary} {self.v22general} {self.v23town}")


def load_data():
    """Load data from newton_voters.csv into the Django database."""

    # Open the file for reading
    filename = "C:/Users/tiffa/Downloads/newton_voters.csv"
    f = open(filename, "r")

    # Discard the header
    f.readline()
    
    # Read the entire file
    for line in f:
        try:
            fields = line.strip().split(",")

            # Create a new instance of the Voter model
            voter = Voter(voter_id=fields[0], 
                          last_name=fields[1], 
                          first_name=fields[2], 
                          street_number=fields[3], 
                          street_name=fields[4], 
                          apartment_number=fields[5], 
                          zip_code=fields[6], 
                          date_of_birth=fields[7], 
                          date_of_registration=fields[8], 
                          party_affiliation=fields[9], 
                          precinct_number=fields[10], 
                          v20state=fields[11] == "TRUE", 
                          v21town=fields[12] == "TRUE", 
                          v21primary=fields[13] == "TRUE", 
                          v22general=fields[14] == "TRUE", 
                          v23town=fields[15] == "TRUE", 
                          voter_score=fields[16])
            voter.save()
        except:
            print("Something went wrong.")
            print(f"line={line}")

    print(f"Done. Created {len(Voter.objects.all())} Voters")