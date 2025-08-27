#!/usr/bin/env python3
"""
GeoIP ACL Networks Downloader

Downloads and processes IP networks for specified countries from multiple GeoIP sources,
removes redundant subnets, and saves them to separate IPv4 and IPv6 files.
"""

import requests
import ipaddress
import logging
import sys
import argparse
from typing import Set, List, Optional
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# Configure logger (will be set up in main)
logger = logging.getLogger(__name__)


class GeoIPACLDownloader:
    """Downloads and processes IP networks for specified countries from GeoIP sources."""
    
    DEFAULT_URLS = [
        "https://geoip.site/download/MaxMind/GeoIP.acl",
        "https://geoip.site/download/IP2Location/GeoIP.acl",
        "https://geoip.site/download/DB-IP/GeoIP.acl"
    ]
    
    def __init__(self, country_code: str, urls: Optional[List[str]] = None, timeout: int = 30):
        """
        Initialize the downloader.
        
        Args:
            country_code: Two-letter country code (e.g., 'BR', 'US', 'CN').
            urls: List of URLs to download from. Uses default if None.
            timeout: Request timeout in seconds.
        """
        self.country_code = country_code.upper()
        self.urls = urls or self.DEFAULT_URLS
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'GeoIP-ACL-Downloader/1.0 (Python) Country/{self.country_code}'
        })
        
    def download_url(self, url: str) -> Optional[str]:
        """
        Download content from a single URL.
        
        Args:
            url: URL to download from.
            
        Returns:
            Downloaded content or None if failed.
        """
        try:
            logger.info(f"Downloading from: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Successfully downloaded {len(response.text)} characters from {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to download from {url}: {e}")
            return None
    
    def parse_acl_content(self, content: str) -> Set[ipaddress.IPv4Network | ipaddress.IPv6Network]:
        """
        Parse ACL content to extract IP networks for the specified country.
        
        Args:
            content: Raw ACL file content.
            
        Returns:
            Set of IP networks found in the content for the specified country.
        """
        networks = set()
        lines = content.split('\n')
        in_country_block = False
        acl_pattern = f"acl {self.country_code}"
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for start of country block
            if acl_pattern in line:
                in_country_block = True
                logger.debug(f"Found {self.country_code} block at line {line_num}")
                continue
            
            # Check for end of block
            if "}" in line and in_country_block:
                in_country_block = False
                logger.debug(f"End of {self.country_code} block at line {line_num}")
                continue
            
            # Process IP networks within country block
            if in_country_block and line:
                ip_str = line.strip(';').strip()
                if ip_str and not ip_str.startswith('#'):  # Skip comments
                    try:
                        ip_obj = ipaddress.ip_network(ip_str, strict=False)
                        networks.add(ip_obj)
                    except ValueError as e:
                        logger.warning(f"Invalid IP network '{ip_str}' at line {line_num}: {e}")
        
        return networks
    
    def download_and_parse_all(self) -> tuple[Set[ipaddress.IPv4Network], Set[ipaddress.IPv6Network]]:
        """
        Download and parse all URLs concurrently.
        
        Returns:
            Tuple of (IPv4 networks, IPv6 networks).
        """
        all_networks = set()
        
        # Download all URLs concurrently
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_url = {executor.submit(self.download_url, url): url for url in self.urls}
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content = future.result()
                    if content:
                        networks = self.parse_acl_content(content)
                        all_networks.update(networks)
                        logger.info(f"Extracted {len(networks)} networks from {url}")
                    else:
                        logger.warning(f"No content received from {url}")
                except Exception as e:
                    logger.error(f"Error processing {url}: {e}")
        
        # Separate IPv4 and IPv6 networks
        ipv4_networks = {net for net in all_networks if net.version == 4}
        ipv6_networks = {net for net in all_networks if net.version == 6}
        
        logger.info(f"Total networks found: {len(all_networks)} "
                   f"(IPv4: {len(ipv4_networks)}, IPv6: {len(ipv6_networks)}) for {self.country_code}")
        
        return ipv4_networks, ipv6_networks
    
    @staticmethod
    def filter_supernets(networks: Set[ipaddress.IPv4Network | ipaddress.IPv6Network]) -> Set[ipaddress.IPv4Network | ipaddress.IPv6Network]:
        """
        Remove subnets that are contained within larger networks.
        
        Args:
            networks: Set of IP networks to filter.
            
        Returns:
            Set of networks with redundant subnets removed.
        """
        if not networks:
            return set()
        
        logger.info(f"Filtering {len(networks)} networks to remove redundant subnets...")
        
        # Convert to sorted list for efficient processing
        sorted_networks = sorted(networks, key=lambda x: (x.network_address, x.prefixlen))
        filtered = set()
        
        for current_net in sorted_networks:
            # Check if current network is a subnet of any network already in filtered set
            is_subnet = any(
                current_net != existing_net and current_net.subnet_of(existing_net)
                for existing_net in filtered
            )
            
            if not is_subnet:
                # Remove any existing networks that are subnets of the current network
                filtered = {
                    net for net in filtered 
                    if not (net != current_net and net.subnet_of(current_net))
                }
                filtered.add(current_net)
        
        reduction = len(networks) - len(filtered)
        logger.info(f"Filtered out {reduction} redundant subnets. {len(filtered)} networks remaining.")
        
        return filtered
    
    def save_networks_to_file(self, networks: Set[ipaddress.IPv4Network | ipaddress.IPv6Network], 
                             filename: str) -> None:
        """
        Save networks to a file.
        
        Args:
            networks: Set of networks to save.
            filename: Output filename.
        """
        if not networks:
            logger.warning(f"No networks to save to {filename}")
            return
        
        try:
            output_path = Path(filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                for net in sorted(networks):
                    f.write(f"{net}\n")
            
            logger.info(f"Saved {len(networks)} networks to {output_path.absolute()}")
        except IOError as e:
            logger.error(f"Failed to save networks to {filename}: {e}")
            raise
    
    def process(self, ipv4_file: Optional[str] = None, ipv6_file: Optional[str] = None) -> None:
        """
        Main processing method - download, parse, filter and save networks.
        
        Args:
            ipv4_file: Output filename for IPv4 networks. Auto-generated if None.
            ipv6_file: Output filename for IPv6 networks. Auto-generated if None.
        """
        start_time = time.time()
        
        # Auto-generate filenames if not provided
        if ipv4_file is None:
            ipv4_file = f'{self.country_code.lower()}_ipv4.txt'
        if ipv6_file is None:
            ipv6_file = f'{self.country_code.lower()}_ipv6.txt'
        
        try:
            # Download and parse all sources
            ipv4_networks, ipv6_networks = self.download_and_parse_all()
            
            if not ipv4_networks and not ipv6_networks:
                logger.error(f"No networks found for country {self.country_code}. "
                           "Check country code and network connectivity.")
                return
            
            # Filter redundant subnets
            if ipv4_networks:
                ipv4_networks = self.filter_supernets(ipv4_networks)
                self.save_networks_to_file(ipv4_networks, ipv4_file)
            
            if ipv6_networks:
                ipv6_networks = self.filter_supernets(ipv6_networks)
                self.save_networks_to_file(ipv6_networks, ipv6_file)
            
            elapsed = time.time() - start_time
            logger.info(f"Processing completed successfully in {elapsed:.2f} seconds")
            logger.info(f"Final results for {self.country_code}: "
                       f"{len(ipv4_networks)} IPv4 networks, {len(ipv6_networks)} IPv6 networks")
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Download and process IP networks for specified countries from GeoIP ACL sources.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --acl BR                    # Download Brazilian IP networks
  %(prog)s --acl US --timeout 60      # Download US networks with 60s timeout
  %(prog)s --acl CN --ipv4 china_v4.txt --ipv6 china_v6.txt
  %(prog)s --acl DE --urls https://example.com/custom.acl
  %(prog)s --acl FR --verbose          # Enable verbose logging

Common country codes:
  BR - Brazil       US - United States    CN - China
  DE - Germany      FR - France          UK - United Kingdom
  JP - Japan        IN - India           RU - Russia
        """
    )
    
    parser.add_argument(
        '--acl', '-a',
        type=str,
        required=True,
        help='Two-letter country code (e.g., BR, US, CN, DE)'
    )
    
    parser.add_argument(
        '--ipv4',
        type=str,
        help='Output filename for IPv4 networks (default: {country}_ipv4.txt)'
    )
    
    parser.add_argument(
        '--ipv6',
        type=str,
        help='Output filename for IPv6 networks (default: {country}_ipv6.txt)'
    )
    
    parser.add_argument(
        '--urls',
        type=str,
        nargs='+',
        help='Custom URLs to download from (space-separated)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        help='Log file path (default: geoip_acl_downloader.log)'
    )
    
    return parser.parse_args()


def setup_logging(verbose: bool = False, log_file: Optional[str] = None):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    log_file = log_file or 'geoip_acl_downloader.log'
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file)
        ]
    )


def main():
    """Main function to run the GeoIP ACL downloader."""
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.verbose, args.log_file)
    
    # Validate country code
    if len(args.acl) != 2:
        logger.error(f"Country code must be exactly 2 characters. Got: '{args.acl}'")
        sys.exit(1)
    
    logger.info(f"Starting GeoIP ACL downloader for country: {args.acl.upper()}")
    
    try:
        downloader = GeoIPACLDownloader(
            country_code=args.acl,
            urls=args.urls,
            timeout=args.timeout
        )
        downloader.process(args.ipv4, args.ipv6)
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
