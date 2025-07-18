import requests
from typing import List, Optional, Dict

class UCSCAPI:
    BASE_URL = "https://api.genome.ucsc.edu/"

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint, params=None):
        """Internal helper for GET requests."""
        url = self.BASE_URL + endpoint
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()

    # 1. List all supported genomes
    def list_genomes(self):
        """Get all supported genome assemblies."""
        return self._get("list/ucscGenomes")

    # 2. List all tracks for a genome
    def list_tracks(self, genome):
        """List all tracks for the given genome."""
        return self._get("list/tracks", params={"genome": genome})
    
    # 3. List all tracks in a hub
    def list_hub_tracks(self, hubUrl, genome):
        """Get all tracks in a given hub/genome."""
        return self._get("list/tracks", params={"hubUrl": hubUrl, "genome": genome})

    # 4. List all chromosomes for a genome
    def list_chroms(self, genome):
        """List all chromosomes for the given genome."""
        return self._get("list/chromosomes", params={"genome": genome})
    
    # 5. List all public track hubs
    def list_hubs(self):
        """Get list of all public UCSC track hubs."""
        return self._get("list/publicHubs")

    # 6. Get chromosome sequence
    def get_chrom_sequence(self, genome, chrom):
        """
        Get chromosome sequence.
        """
        params = {
            "genome": genome,
            "chrom": chrom,
        }
        return self._get("getData/sequence", params=params)

    # 7. Get DNA sequence for a region
    def get_sequence(self, genome, chrom, start=None, end=None, revcomp=False, hubUrl=None):
        """
        Get DNA sequence for a specified region.
        """
        params = {
            "genome": genome,
            "chrom": chrom,
        }
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if revcomp:
            params["revComp"] = 1
        if hubUrl:
            params["hubUrl"] = hubUrl

        return self._get("getData/sequence", params=params)

    # 8. Get data for a track
    def get_track_data(self, genome, track, chrom=None, start=None, end=None, maxItemsOutput=None):
        """
        Get track data (annotation) for a specified region.
        """
        params = {
            "genome": genome,
            "track": track,
        }
        if chrom:
            params["chrom"] = chrom
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if maxItemsOutput:
            params["maxItemsOutput"] = maxItemsOutput

        return self._get("getData/track", params=params)


    # 9. Get cytoband info
    def get_cytoband(self, genome, chrom=None):
        """Get cytoband (chromosome banding) information."""
        params = {"genome": genome}
        if chrom:
            params["chrom"] = chrom
        return self._get("getData/cytoband", params=params)


if __name__ == "__main__":
    api = UCSCAPI()
    print("Supported Genomes:", api.list_genomes())
    print("Tracks for hg38:", api.list_tracks("hg38"))
    print("Chromosomes for hg38:", api.list_chroms("hg38"))
    seq = api.get_sequence("hg38", "chrM", start=0, end=100)
    print("chrM:1-100 sequence:", seq['dna'])
    gold = api.get_track_data("hg38", "gold", chrom="chr1", start=47000, end=48000)
    print("Gold track chr1:47000-48000:", gold)