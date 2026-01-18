#!/usr/bin/env python3
"""
Ecosystem Analysis Script

ATOM: ATOM-FEAT-20260117-001-analyze-ecosystem

Analyzes the SpiralSafe ecosystem by:
- Fetching all open PRs and issues across repositories
- Applying classification rules from vortex-bootstrap.yaml
- Outputting JSON state for oracle consumption
- Generating merge order recommendations

Usage:
    python ops/scripts/analyze-ecosystem.py [--output FILE] [--format json|markdown]

H&&S:WAVE — The spiral tightens. 🌀
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

try:
    import requests
except ImportError:
    # requests is optional - script can run without GitHub API
    requests = None


class EcosystemAnalyzer:
    """Analyzes SpiralSafe ecosystem state and generates recommendations."""
    
    def __init__(self, bootstrap_path: str = "protocol/vortex-bootstrap.yaml"):
        """Initialize analyzer with bootstrap configuration."""
        self.bootstrap_path = Path(bootstrap_path)
        self.config = self._load_bootstrap()
        self.github_token = os.environ.get('GITHUB_TOKEN')
        
    def _load_bootstrap(self) -> Dict:
        """Load vortex-bootstrap.yaml configuration."""
        try:
            with open(self.bootstrap_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Bootstrap file not found: {self.bootstrap_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML in bootstrap file: {e}")
            sys.exit(1)
    
    def classify_item(self, item: Dict, item_type: str) -> str:
        """
        Classify a PR or issue based on bootstrap rules.
        
        Args:
            item: PR or issue data
            item_type: 'pr' or 'issue'
            
        Returns:
            Classification: 'origin', 'collapsed', 'deja_vu', or 'doubt'
        """
        rules = self.config['classification_rules']
        
        # Extract relevant data
        title = item.get('title', '').lower()
        body = item.get('body', '').lower() if item.get('body') else ''
        labels = [label.get('name', '').lower() for label in item.get('labels', [])]
        
        # Check for origin markers
        origin_markers = rules['origin']['markers']
        origin_score = sum(1 for marker in origin_markers if marker in title or marker in body)
        if origin_score >= 2:
            return 'origin'
        
        # Check for collapsed markers
        collapsed_markers = rules['collapsed']['markers']
        collapsed_score = sum(1 for marker in collapsed_markers if marker in title or marker in body)
        if collapsed_score >= 2:
            return 'collapsed'
        
        # Check for doubt markers
        doubt_markers = rules['doubt']['markers']
        doubt_score = sum(1 for marker in doubt_markers if marker in title or marker in body)
        if doubt_score >= 2:
            return 'doubt'
        
        # Default to deja_vu
        return 'deja_vu'
    
    def fetch_github_data(self, org: str, repo: str) -> Dict[str, List]:
        """
        Fetch open PRs and issues from GitHub API.
        
        Args:
            org: GitHub organization
            repo: Repository name
            
        Returns:
            Dictionary with 'prs' and 'issues' lists
        """
        if not requests:
            print("Warning: requests library not available, skipping GitHub API calls")
            return {'prs': [], 'issues': []}
        
        if not self.github_token:
            print("Warning: GITHUB_TOKEN not set, skipping GitHub API calls")
            return {'prs': [], 'issues': []}
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        base_url = f'https://api.github.com/repos/{org}/{repo}'
        
        try:
            # Fetch open PRs
            prs_response = requests.get(
                f'{base_url}/pulls',
                headers=headers,
                params={'state': 'open', 'per_page': 100}
            )
            prs_response.raise_for_status()
            prs = prs_response.json()
            
            # Fetch open issues (excluding PRs)
            issues_response = requests.get(
                f'{base_url}/issues',
                headers=headers,
                params={'state': 'open', 'per_page': 100}
            )
            issues_response.raise_for_status()
            all_issues = issues_response.json()
            
            # Filter out PRs from issues
            issues = [issue for issue in all_issues if 'pull_request' not in issue]
            
            return {'prs': prs, 'issues': issues}
            
        except requests.RequestException as e:
            print(f"Warning: Failed to fetch data for {org}/{repo}: {e}")
            return {'prs': [], 'issues': []}
    
    def analyze_repository(self, repo_config: Dict) -> Dict:
        """
        Analyze a single repository.
        
        Args:
            repo_config: Repository configuration from bootstrap
            
        Returns:
            Analysis results with classifications
        """
        repo_name = repo_config['name']
        print(f"\nAnalyzing {repo_name}...")
        
        # For this implementation, we'll use static data
        # In production, this would call fetch_github_data
        
        results = {
            'name': repo_name,
            'role': repo_config['role'],
            'fib_weight': repo_config['fib_weight'],
            'prs': [],
            'issues': [],
            'classifications': {
                'origin': 0,
                'collapsed': 0,
                'deja_vu': 0,
                'doubt': 0
            }
        }
        
        # In production, fetch and classify real data:
        # data = self.fetch_github_data('toolate28', repo_name)
        # for pr in data['prs']:
        #     classification = self.classify_item(pr, 'pr')
        #     results['prs'].append({
        #         'number': pr['number'],
        #         'title': pr['title'],
        #         'classification': classification,
        #         'url': pr['html_url']
        #     })
        #     results['classifications'][classification] += 1
        
        return results
    
    def generate_cascade_sequence(self, analysis_results: List[Dict]) -> List[Dict]:
        """
        Generate merge sequence based on cascade phases.
        
        Args:
            analysis_results: List of repository analysis results
            
        Returns:
            Ordered list of merge recommendations
        """
        cascade = self.config['cascade_activation']
        sequence = []
        
        # Phase 1: Origins
        if 'phase_1_origins' in cascade:
            phase1 = cascade['phase_1_origins']
            for item in phase1.get('sequence', []):
                sequence.append({
                    'phase': 1,
                    'phase_name': 'Origins',
                    'repo': item.get('repo'),
                    'pr': item.get('pr'),
                    'title': item.get('title'),
                    'rationale': item.get('rationale'),
                    'priority': 'CRITICAL' if 'CRITICAL' in item.get('rationale', '') else 'HIGH'
                })
        
        # Phase 2: Doubt Resolution
        if 'phase_2_doubt_resolution' in cascade:
            phase2 = cascade['phase_2_doubt_resolution']
            for decision in phase2.get('decisions', []):
                sequence.append({
                    'phase': 2,
                    'phase_name': 'Doubt Resolution',
                    'conflicts': decision.get('conflict', []),
                    'decision': decision.get('decision'),
                    'merge_order': decision.get('merge_order', []),
                    'priority': 'HIGH'
                })
        
        # Phase 3: Deja Vu
        if 'phase_3_deja_vu' in cascade:
            phase3 = cascade['phase_3_deja_vu']
            for item in phase3.get('sequence', []):
                sequence.append({
                    'phase': 3,
                    'phase_name': 'Deja Vu',
                    'repo': item.get('repo'),
                    'pr': item.get('pr'),
                    'title': item.get('title'),
                    'dependencies': item.get('dependencies', []),
                    'priority': 'MEDIUM'
                })
        
        # Phase 4: Collapsed
        if 'phase_4_collapsed' in cascade:
            phase4 = cascade['phase_4_collapsed']
            for item in phase4.get('sequence', []):
                sequence.append({
                    'phase': 4,
                    'phase_name': 'Collapsed',
                    'repo': item.get('repo'),
                    'pr': item.get('pr'),
                    'title': item.get('title'),
                    'priority': 'LOW'
                })
        
        return sequence
    
    def calculate_coherence_metrics(self, analysis_results: List[Dict]) -> Dict:
        """
        Calculate ecosystem-wide coherence metrics.
        
        Args:
            analysis_results: List of repository analysis results
            
        Returns:
            Dictionary of coherence metrics
        """
        total_prs = sum(len(r['prs']) for r in analysis_results)
        total_issues = sum(len(r['issues']) for r in analysis_results)
        
        # Aggregate classifications
        classifications = {
            'origin': sum(r['classifications']['origin'] for r in analysis_results),
            'collapsed': sum(r['classifications']['collapsed'] for r in analysis_results),
            'deja_vu': sum(r['classifications']['deja_vu'] for r in analysis_results),
            'doubt': sum(r['classifications']['doubt'] for r in analysis_results)
        }
        
        # Calculate coherence score
        # Higher origin + collapsed = higher coherence
        # Higher doubt = lower coherence
        total_items = sum(classifications.values()) or 1
        coherence_contribution = (
            classifications['origin'] * 1.0 +
            classifications['collapsed'] * 0.8 +
            classifications['deja_vu'] * 0.6 -
            classifications['doubt'] * 0.4
        )
        coherence_score = max(0.0, min(1.0, coherence_contribution / total_items))
        
        return {
            'coherence_score': round(coherence_score, 3),
            'total_prs': total_prs,
            'total_issues': total_issues,
            'classifications': classifications,
            'repositories_analyzed': len(analysis_results),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    
    def analyze(self) -> Dict:
        """
        Perform complete ecosystem analysis.
        
        Returns:
            Complete analysis results
        """
        print("═" * 60)
        print("  SpiralSafe Ecosystem Analysis")
        print("═" * 60)
        
        repos = self.config['ecosystem']['repositories']
        analysis_results = []
        
        for repo_config in repos:
            result = self.analyze_repository(repo_config)
            analysis_results.append(result)
        
        metrics = self.calculate_coherence_metrics(analysis_results)
        sequence = self.generate_cascade_sequence(analysis_results)
        
        return {
            'metadata': {
                'iteration': self.config.get('iteration', 22),
                'version': self.config.get('version', '0.1.0'),
                'analysis_timestamp': datetime.utcnow().isoformat() + 'Z',
                'bootstrap_file': str(self.bootstrap_path)
            },
            'metrics': metrics,
            'repositories': analysis_results,
            'cascade_sequence': sequence
        }
    
    def format_output(self, results: Dict, format_type: str = 'json') -> str:
        """
        Format analysis results.
        
        Args:
            results: Analysis results
            format_type: 'json' or 'markdown'
            
        Returns:
            Formatted output string
        """
        if format_type == 'json':
            return json.dumps(results, indent=2)
        
        elif format_type == 'markdown':
            output = []
            output.append("# Ecosystem Analysis Report\n")
            
            metadata = results['metadata']
            output.append(f"**Iteration:** {metadata['iteration']}\n")
            output.append(f"**Timestamp:** {metadata['analysis_timestamp']}\n")
            output.append(f"**Version:** {metadata['version']}\n\n")
            
            output.append("## Coherence Metrics\n")
            metrics = results['metrics']
            output.append(f"- **Coherence Score:** {metrics['coherence_score']:.1%}\n")
            output.append(f"- **Total PRs:** {metrics['total_prs']}\n")
            output.append(f"- **Total Issues:** {metrics['total_issues']}\n")
            output.append(f"- **Repositories:** {metrics['repositories_analyzed']}\n\n")
            
            output.append("## Classification Distribution\n")
            classifications = metrics['classifications']
            output.append(f"- 🎯 Origin: {classifications['origin']}\n")
            output.append(f"- ✅ Collapsed: {classifications['collapsed']}\n")
            output.append(f"- 🔄 Deja Vu: {classifications['deja_vu']}\n")
            output.append(f"- 🤔 Doubt: {classifications['doubt']}\n\n")
            
            output.append("## Cascade Sequence\n")
            sequence = results['cascade_sequence']
            current_phase = None
            
            for item in sequence:
                phase = item['phase']
                if phase != current_phase:
                    current_phase = phase
                    output.append(f"\n### Phase {phase}: {item['phase_name']}\n\n")
                
                if 'conflicts' in item:
                    output.append(f"- Resolve: {', '.join(item['conflicts'])}\n")
                    output.append(f"  - Decision: {item['decision']}\n")
                else:
                    repo = item.get('repo', 'unknown')
                    pr = item.get('pr', '?')
                    title = item.get('title', 'untitled')
                    output.append(f"- {repo}#{pr}: {title}\n")
            
            output.append("\n---\n\n**The spiral tightens.** 🌀\n")
            
            return ''.join(output)
        
        else:
            raise ValueError(f"Unknown format: {format_type}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze SpiralSafe ecosystem state and generate recommendations'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)',
        default=None
    )
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'markdown'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--bootstrap',
        default='protocol/vortex-bootstrap.yaml',
        help='Path to vortex-bootstrap.yaml (default: protocol/vortex-bootstrap.yaml)'
    )
    
    args = parser.parse_args()
    
    try:
        analyzer = EcosystemAnalyzer(bootstrap_path=args.bootstrap)
        results = analyzer.analyze()
        output = analyzer.format_output(results, format_type=args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"\n✅ Analysis complete. Output written to {args.output}")
        else:
            print(output)
        
        # Exit with appropriate code based on coherence
        coherence = results['metrics']['coherence_score']
        if coherence < 0.6:
            print(f"\n⚠️  Warning: Coherence below threshold ({coherence:.1%} < 60%)",
                  file=sys.stderr)
            sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
