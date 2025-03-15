#!/usr/bin/env python3
"""
Example client demonstrating how to use the YouTube API Server
"""
import argparse
import json
import requests

def get_video_data(api_url, video_url):
    """
    Retrieves metadata for a YouTube video
    
    Args:
        api_url (str): Base URL of the API
        video_url (str): YouTube video URL
        
    Returns:
        dict: Video metadata
    """
    endpoint = f"{api_url}/youtube/video-data"
    payload = {"url": video_url}
    
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    
    return response.json()

def get_video_captions(api_url, video_url, languages=None):
    """
    Retrieves captions for a YouTube video
    
    Args:
        api_url (str): Base URL of the API
        video_url (str): YouTube video URL
        languages (list): Optional list of language codes
        
    Returns:
        str: Video captions
    """
    endpoint = f"{api_url}/youtube/video-captions"
    payload = {"url": video_url}
    
    if languages:
        payload["languages"] = languages
    
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    
    return response.text

def get_video_timestamps(api_url, video_url, languages=None):
    """
    Retrieves timestamped captions for a YouTube video
    
    Args:
        api_url (str): Base URL of the API
        video_url (str): YouTube video URL
        languages (list): Optional list of language codes
        
    Returns:
        list: Timestamped captions
    """
    endpoint = f"{api_url}/youtube/video-timestamps"
    payload = {"url": video_url}
    
    if languages:
        payload["languages"] = languages
    
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="YouTube API Client Example")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--api", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--type", choices=["data", "captions", "timestamps"], 
                        default="data", help="Type of data to retrieve")
    parser.add_argument("--languages", nargs="+", help="Language codes for captions")
    
    args = parser.parse_args()
    
    try:
        if args.type == "data":
            result = get_video_data(args.api, args.url)
            print(json.dumps(result, indent=2))
        elif args.type == "captions":
            result = get_video_captions(args.api, args.url, args.languages)
            print(result)
        elif args.type == "timestamps":
            result = get_video_timestamps(args.api, args.url, args.languages)
            for timestamp in result:
                print(timestamp)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
