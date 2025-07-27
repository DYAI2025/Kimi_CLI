#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code Analyzer for Kimi K2 Agent
Advanced static code analysis and quality assessment
"""

import ast
import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class CodeAnalyzer:
    """Advanced code analyzer for multiple programming languages"""
    
    def __init__(self):
        self.supported_languages = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php'
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a code file for various metrics and issues
        
        Args:
            file_path: Path to the code file
            
        Returns:
            Analysis results dictionary
        """
        try:
            extension = Path(file_path).suffix.lower()
            language = self.supported_languages.get(extension, 'unknown')
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'file_path': file_path,
                'language': language,
                'metrics': self._calculate_metrics(content),
                'issues': self._detect_issues(content, language),
                'complexity': self._calculate_complexity(content, language),
                'security': self._security_check(content, language),
                'quality_score': 0  # Will be calculated
            }
            
            # Calculate overall quality score
            analysis['quality_score'] = self._calculate_quality_score(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e),
                'quality_score': 0
            }
    
    def _calculate_metrics(self, content: str) -> Dict[str, int]:
        """Calculate basic code metrics"""
        lines = content.split('\n')
        
        return {
            'total_lines': len(lines),
            'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'max_line_length': max(len(line) for line in lines) if lines else 0,
            'avg_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0
        }
    
    def _detect_issues(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Detect potential code issues"""
        issues = []
        
        if language == 'python':
            issues.extend(self._detect_python_issues(content))
        elif language in ['javascript', 'typescript']:
            issues.extend(self._detect_js_issues(content))
        
        # Common issues for all languages
        issues.extend(self._detect_common_issues(content))
        
        return issues
    
    def _detect_python_issues(self, content: str) -> List[Dict[str, Any]]:
        """Detect Python-specific issues"""
        issues = []
        lines = content.split('\n')
        
        try:
            # Parse AST for advanced analysis
            tree = ast.parse(content)
            
            # Check for potential issues
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Function too long
                    if hasattr(node, 'end_lineno') and node.end_lineno - node.lineno > 50:
                        issues.append({
                            'type': 'complexity',
                            'severity': 'warning',
                            'line': node.lineno,
                            'message': f'Function "{node.name}" is too long ({node.end_lineno - node.lineno} lines)'
                        })
                    
                    # Too many parameters
                    if len(node.args.args) > 5:
                        issues.append({
                            'type': 'complexity',
                            'severity': 'warning',
                            'line': node.lineno,
                            'message': f'Function "{node.name}" has too many parameters ({len(node.args.args)})'
                        })
                
                elif isinstance(node, ast.ClassDef):
                    # Class too large (simple heuristic)
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    if len(methods) > 20:
                        issues.append({
                            'type': 'complexity',
                            'severity': 'warning',
                            'line': node.lineno,
                            'message': f'Class "{node.name}" has too many methods ({len(methods)})'
                        })
        
        except SyntaxError as e:
            issues.append({
                'type': 'syntax',
                'severity': 'error',
                'line': e.lineno,
                'message': f'Syntax error: {e.msg}'
            })
        
        # Check for common Python anti-patterns
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Bare except
            if 'except:' in stripped and not stripped.endswith('except:'):
                issues.append({
                    'type': 'best_practice',
                    'severity': 'warning',
                    'line': i,
                    'message': 'Bare except clause - specify exception type'
                })
            
            # Print statements (should use logging)
            if 'print(' in stripped and not stripped.startswith('#'):
                issues.append({
                    'type': 'best_practice',
                    'severity': 'info',
                    'line': i,
                    'message': 'Consider using logging instead of print'
                })
        
        return issues
    
    def _detect_js_issues(self, content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript/TypeScript-specific issues"""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # == instead of ===
            if '==' in stripped and '===' not in stripped and '!=' in stripped:
                issues.append({
                    'type': 'best_practice',
                    'severity': 'warning',
                    'line': i,
                    'message': 'Use === instead of == for strict equality'
                })
            
            # var instead of let/const
            if stripped.startswith('var '):
                issues.append({
                    'type': 'best_practice',
                    'severity': 'info',
                    'line': i,
                    'message': 'Consider using let or const instead of var'
                })
            
            # console.log (should be removed in production)
            if 'console.log(' in stripped:
                issues.append({
                    'type': 'best_practice',
                    'severity': 'info',
                    'line': i,
                    'message': 'Remove console.log in production code'
                })
        
        return issues
    
    def _detect_common_issues(self, content: str) -> List[Dict[str, Any]]:
        """Detect issues common to all languages"""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Long lines
            if len(line) > 120:
                issues.append({
                    'type': 'style',
                    'severity': 'info',
                    'line': i,
                    'message': f'Line too long ({len(line)} characters)'
                })
            
            # Trailing whitespace
            if line.rstrip() != line:
                issues.append({
                    'type': 'style',
                    'severity': 'info',
                    'line': i,
                    'message': 'Trailing whitespace'
                })
            
            # Mixed tabs and spaces (simplified check)
            if '\t' in line and '    ' in line:
                issues.append({
                    'type': 'style',
                    'severity': 'warning',
                    'line': i,
                    'message': 'Mixed tabs and spaces'
                })
        
        return issues
    
    def _calculate_complexity(self, content: str, language: str) -> Dict[str, Any]:
        """Calculate cyclomatic complexity"""
        complexity = {
            'cyclomatic': 1,  # Base complexity
            'cognitive': 0,
            'depth': 0
        }
        
        # Simple complexity calculation based on control structures
        control_keywords = ['if', 'else', 'elif', 'for', 'while', 'try', 'except', 'case', 'switch']
        
        for keyword in control_keywords:
            # Count occurrences (simplified)
            complexity['cyclomatic'] += content.count(f' {keyword} ') + content.count(f'{keyword}(')
        
        return complexity
    
    def _security_check(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Basic security vulnerability check"""
        security_issues = []
        
        # Common security patterns
        security_patterns = {
            'sql_injection': [r'execute\s*\(\s*["\'].*%.*["\']', r'query\s*\(\s*["\'].*\+'],
            'xss': [r'innerHTML\s*=', r'document\.write\s*\('],
            'hardcoded_secrets': [r'password\s*=\s*["\'][^"\']+["\']', r'api_key\s*=\s*["\'][^"\']+["\']'],
            'unsafe_eval': [r'eval\s*\(', r'exec\s*\('],
        }
        
        lines = content.split('\n')
        for category, patterns in security_patterns.items():
            for pattern in patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        security_issues.append({
                            'type': 'security',
                            'category': category,
                            'severity': 'high',
                            'line': i,
                            'message': f'Potential {category.replace("_", " ")} vulnerability'
                        })
        
        return security_issues
    
    def _calculate_quality_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall quality score (0-100)"""
        if 'error' in analysis:
            return 0
        
        score = 100
        metrics = analysis.get('metrics', {})
        issues = analysis.get('issues', [])
        security = analysis.get('security', [])
        
        # Deduct points for issues
        for issue in issues:
            if issue['severity'] == 'error':
                score -= 20
            elif issue['severity'] == 'warning':
                score -= 5
            elif issue['severity'] == 'info':
                score -= 1
        
        # Deduct points for security issues
        score -= len(security) * 15
        
        # Bonus for good metrics
        if metrics.get('code_lines', 0) > 0:
            comment_ratio = metrics.get('comment_lines', 0) / metrics['code_lines']
            if comment_ratio > 0.1:  # Good comment coverage
                score += 5
        
        return max(0, min(100, score))