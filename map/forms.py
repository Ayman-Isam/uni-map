from django import forms
from .models import Marker
from urllib.parse import urlparse, parse_qs

def get_lat_lng_from_gmaps_url(url):
   at_index = url.find('@')
   comma_index = url.find(',', at_index)
   if at_index != -1 and comma_index != -1:
       lat = url[at_index + 1:comma_index]
       lon_start = url.find(',', comma_index + 1)
       if lon_start != -1:
           lon = url[comma_index + 1:lon_start]
           return float(lat), float(lon)
   return None, None

class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = ['name', 'map_url', 'location', 'website', 'program','contact', 'scholarship', 'logo' ]

    def clean(self):
        cleaned_data = super().clean()
        map_url = cleaned_data.get('map_url')
        if map_url:
            lat, lng = get_lat_lng_from_gmaps_url(map_url)
            if lat is None or lng is None:
                raise forms.ValidationError("Invalid Google Maps URL")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        map_url = self.cleaned_data.get('map_url')
        if map_url:
            lat, lng = get_lat_lng_from_gmaps_url(map_url)
            instance.lat = lat
            instance.lng = lng
        if commit:
            instance.save()
        return instance