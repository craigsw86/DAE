#!/usr/bin/env python3
"""
IR Training Simulator
Comprehensive incident response training simulation tool
"""

import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import argparse
import sys

class IRTrainingSimulator:
    def __init__(self, config_file: str = None):
        """Initialize the IR Training Simulator"""
        self.config = self.load_config(config_file)
        self.scenarios = self.load_scenarios()
        self.participants = []
        self.current_scenario = None
        self.start_time = None
        self.performance_data = {}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ir_training.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "exercise_duration": 240,  # 4 hours
            "inject_interval": 15,     # 15 minutes
            "evaluation_criteria": {
                "detection_time": 300,      # 5 minutes
                "containment_time": 900,    # 15 minutes
                "communication_time": 600,  # 10 minutes
                "evidence_handling": 0.95   # 95% accuracy
            },
            "scoring_weights": {
                "detection": 0.25,
                "containment": 0.25,
                "communication": 0.25,
                "evidence_handling": 0.25
            }
        }
        
        if config_file:
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            except FileNotFoundError:
                self.logger.warning(f"Config file {config_file} not found, using defaults")
        
        return default_config
    
    def load_scenarios(self) -> Dict[str, Any]:
        """Load training scenarios"""
        scenarios = {
            "ransomware_attack": {
                "name": "Ransomware Attack with Data Exfiltration",
                "difficulty": "intermediate",
                "duration": 240,
                "injects": [
                    {
                        "time": 0,
                        "type": "detection",
                        "content": "SIEM alerts show multiple failed login attempts from unknown IP 203.45.67.89",
                        "expected_response": "classify_incident"
                    },
                    {
                        "time": 15,
                        "type": "escalation",
                        "content": "Successful login detected, attempts to access PHI database blocked",
                        "expected_response": "escalate_incident"
                    },
                    {
                        "time": 45,
                        "type": "data_access",
                        "content": "PHI database accessed, patient records being queried",
                        "expected_response": "contain_breach"
                    },
                    {
                        "time": 120,
                        "type": "ransomware",
                        "content": "Ransomware deployed across multiple servers, ransom note displayed",
                        "expected_response": "activate_crisis_management"
                    },
                    {
                        "time": 180,
                        "type": "crisis",
                        "content": "Media inquiry received, attackers posting on social media",
                        "expected_response": "manage_crisis_communication"
                    }
                ]
            },
            "insider_threat": {
                "name": "Insider Threat with Data Exfiltration",
                "difficulty": "advanced",
                "duration": 180,
                "injects": [
                    {
                        "time": 0,
                        "type": "suspicious_activity",
                        "content": "Employee John Smith accessing patient records outside business hours",
                        "expected_response": "investigate_activity"
                    },
                    {
                        "time": 30,
                        "type": "evidence_collection",
                        "content": "USB drive found with thousands of patient records, selling to identity thieves",
                        "expected_response": "preserve_evidence"
                    },
                    {
                        "time": 90,
                        "type": "legal_proceedings",
                        "content": "Employee arrested, large-scale identity theft operation discovered",
                        "expected_response": "coordinate_with_law_enforcement"
                    }
                ]
            },
            "apt_attack": {
                "name": "Advanced Persistent Threat (APT)",
                "difficulty": "expert",
                "duration": 480,
                "injects": [
                    {
                        "time": 0,
                        "type": "ioc_detection",
                        "content": "Threat intelligence identifies IOCs associated with known APT group",
                        "expected_response": "investigate_iocs"
                    },
                    {
                        "time": 120,
                        "type": "confirmed_compromise",
                        "content": "Confirmed compromise, attackers in network for weeks, established persistence",
                        "expected_response": "activate_incident_response"
                    },
                    {
                        "time": 360,
                        "type": "data_exfiltration",
                        "content": "Active PHI data exfiltration detected, encrypted channels used",
                        "expected_response": "stop_exfiltration"
                    },
                    {
                        "time": 420,
                        "type": "crisis_management",
                        "content": "Attackers claim responsibility, threaten to release patient data publicly",
                        "expected_response": "manage_crisis"
                    }
                ]
            }
        }
        return scenarios
    
    def register_participant(self, name: str, role: str, experience_level: str):
        """Register a participant in the training exercise"""
        participant = {
            "name": name,
            "role": role,
            "experience_level": experience_level,
            "actions": [],
            "score": 0
        }
        self.participants.append(participant)
        self.logger.info(f"Registered participant: {name} ({role})")
    
    def start_scenario(self, scenario_name: str):
        """Start a training scenario"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario {scenario_name} not found")
        
        self.current_scenario = self.scenarios[scenario_name]
        self.start_time = datetime.now()
        self.performance_data = {
            "scenario": scenario_name,
            "start_time": self.start_time.isoformat(),
            "participants": len(self.participants),
            "actions": [],
            "scores": {}
        }
        
        self.logger.info(f"Started scenario: {self.current_scenario['name']}")
        self.logger.info(f"Participants: {len(self.participants)}")
        
        # Start the scenario
        self.run_scenario()
    
    def run_scenario(self):
        """Run the current scenario"""
        scenario = self.current_scenario
        total_duration = scenario['duration']
        
        self.logger.info(f"Running scenario for {total_duration} minutes")
        
        for inject in scenario['injects']:
            # Wait for inject time
            if inject['time'] > 0:
                time.sleep(inject['time'] * 60)  # Convert to seconds
            
            # Present inject
            self.present_inject(inject)
            
            # Collect responses
            self.collect_responses(inject)
        
        # End scenario
        self.end_scenario()
    
    def present_inject(self, inject: Dict[str, Any]):
        """Present an inject to participants"""
        inject_time = datetime.now() - self.start_time
        self.logger.info(f"INJECT at {inject_time}: {inject['content']}")
        
        # Record inject
        self.performance_data['actions'].append({
            "time": inject_time.total_seconds(),
            "type": "inject",
            "content": inject['content'],
            "expected_response": inject['expected_response']
        })
    
    def collect_responses(self, inject: Dict[str, Any]):
        """Collect responses from participants"""
        print(f"\n{'='*60}")
        print(f"INJECT: {inject['content']}")
        print(f"Expected Response: {inject['expected_response']}")
        print(f"{'='*60}")
        
        # Simulate participant responses
        for participant in self.participants:
            response = self.simulate_response(participant, inject)
            self.record_action(participant, response, inject)
    
    def simulate_response(self, participant: Dict[str, Any], inject: Dict[str, Any]) -> str:
        """Simulate a participant response"""
        # Simple simulation based on experience level
        experience_levels = {
            "beginner": 0.6,
            "intermediate": 0.8,
            "advanced": 0.9,
            "expert": 0.95
        }
        
        success_rate = experience_levels.get(participant['experience_level'], 0.7)
        
        if random.random() < success_rate:
            return f"Correct response to {inject['type']}"
        else:
            return f"Incorrect response to {inject['type']}"
    
    def record_action(self, participant: Dict[str, Any], response: str, inject: Dict[str, Any]):
        """Record a participant action"""
        action = {
            "participant": participant['name'],
            "time": (datetime.now() - self.start_time).total_seconds(),
            "response": response,
            "inject_type": inject['type'],
            "correct": "Correct" in response
        }
        
        participant['actions'].append(action)
        self.performance_data['actions'].append(action)
        
        self.logger.info(f"{participant['name']}: {response}")
    
    def end_scenario(self):
        """End the current scenario"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        self.logger.info(f"Scenario ended after {duration}")
        
        # Calculate scores
        self.calculate_scores()
        
        # Generate report
        self.generate_report()
    
    def calculate_scores(self):
        """Calculate participant scores"""
        for participant in self.participants:
            actions = participant['actions']
            correct_actions = sum(1 for action in actions if action['correct'])
            total_actions = len(actions)
            
            if total_actions > 0:
                accuracy = correct_actions / total_actions
                participant['score'] = accuracy * 100
                
                # Calculate response time
                response_times = [action['time'] for action in actions]
                avg_response_time = sum(response_times) / len(response_times) if response_times else 0
                participant['avg_response_time'] = avg_response_time
                
                self.performance_data['scores'][participant['name']] = {
                    'accuracy': accuracy,
                    'avg_response_time': avg_response_time,
                    'total_actions': total_actions
                }
    
    def generate_report(self):
        """Generate training report"""
        report = {
            "scenario": self.current_scenario['name'],
            "duration": (datetime.now() - self.start_time).total_seconds(),
            "participants": len(self.participants),
            "scores": self.performance_data['scores'],
            "recommendations": self.generate_recommendations()
        }
        
        # Save report
        report_file = f"ir_training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Training report saved to {report_file}")
        
        # Print summary
        self.print_summary(report)
    
    def generate_recommendations(self) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        for participant in self.participants:
            if participant['score'] < 70:
                recommendations.append(f"{participant['name']} needs additional training in incident response")
            
            if participant.get('avg_response_time', 0) > 300:  # 5 minutes
                recommendations.append(f"{participant['name']} should improve response time")
        
        if not recommendations:
            recommendations.append("All participants performed well, consider advanced scenarios")
        
        return recommendations
    
    def print_summary(self, report: Dict[str, Any]):
        """Print training summary"""
        print(f"\n{'='*60}")
        print("TRAINING EXERCISE SUMMARY")
        print(f"{'='*60}")
        print(f"Scenario: {report['scenario']}")
        print(f"Duration: {report['duration']:.1f} seconds")
        print(f"Participants: {report['participants']}")
        print(f"\nScores:")
        
        for name, score_data in report['scores'].items():
            print(f"  {name}: {score_data['accuracy']:.1%} accuracy, "
                  f"{score_data['avg_response_time']:.1f}s avg response time")
        
        print(f"\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
        print(f"{'='*60}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='IR Training Simulator')
    parser.add_argument('--scenario', choices=['ransomware_attack', 'insider_threat', 'apt_attack'],
                       default='ransomware_attack', help='Scenario to run')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--participants', type=int, default=4, help='Number of participants')
    
    args = parser.parse_args()
    
    # Create simulator
    simulator = IRTrainingSimulator(args.config)
    
    # Register participants
    roles = ['Incident Response Lead', 'System Administrator', 'Compliance Officer', 'Communications Manager']
    experience_levels = ['beginner', 'intermediate', 'advanced', 'expert']
    
    for i in range(args.participants):
        name = f"Participant_{i+1}"
        role = roles[i % len(roles)]
        experience = experience_levels[i % len(experience_levels)]
        simulator.register_participant(name, role, experience)
    
    # Start scenario
    try:
        simulator.start_scenario(args.scenario)
    except KeyboardInterrupt:
        print("\nTraining exercise interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
