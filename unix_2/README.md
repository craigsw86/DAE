# UNIX 2 - Course README

## Course Overview
This course builds upon fundamental UNIX/Linux skills by introducing advanced command-line operations, shell management, and environment customization. Students learn to work with multiple arguments, manage different shells, and customize their terminal environment for improved productivity and efficiency.

## Learning Objectives
- Master advanced UNIX command-line operations
- Learn to work with multiple arguments and command options
- Understand shell management and switching between different shells
- Develop skills in environment customization and alias creation
- Build efficient command-line workflows
- Customize terminal environment for professional development

## Course Rubric Requirements

### 1. Commands
- Use of the cp, mkdir, less, mv, rm commands
- Demonstrate proper command syntax and usage
- Show evidence of command execution and output
- Document command purposes and functionality
- Provide examples of command usage in different contexts
- Show evidence of command combination and advanced usage

### 2. Arguments
- Add multiple arguments to a command and add an argument to an option
- Demonstrate understanding of command-line arguments
- Show evidence of multiple argument usage
- Document different types of arguments and their effects
- Provide examples of argument combinations
- Show evidence of option arguments and their functionality

### 3. Kernels and Shells
- Access the default Shell, access the current shell and switch to another shell
- Demonstrate shell identification and management
- Show evidence of shell switching capabilities
- Document different shell types and their characteristics
- Provide examples of shell-specific features
- Show evidence of shell environment management

### 4. Environment
- Create an alias and customize the terminal prompt
- Demonstrate alias creation and management
- Show evidence of prompt customization
- Document environment variable usage
- Provide examples of custom aliases and functions
- Show evidence of persistent environment configuration

## Application to HIPAA Checklist Project

### File Management Operations
- **Project Organization**: Directory structure management for HIPAA compliance project
- **Configuration Files**: Management of project configuration and environment files
- **Backup Operations**: File backup and recovery procedures for healthcare data
- **Documentation**: Text file management and documentation creation
- **Log Files**: System and application log management and analysis

### Advanced Command Usage
- **Batch Operations**: Multiple file operations for compliance data processing
- **Directory Management**: Complex directory structure creation and management
- **File Processing**: Advanced file manipulation for healthcare compliance data
- **System Administration**: Advanced system management tasks
- **Automation**: Shell scripting for automated compliance tasks

### Shell Management for Development
- **Development Environment**: Shell configuration for healthcare application development
- **Script Execution**: Different shell environments for various automation tasks
- **Environment Isolation**: Separate shell environments for different project components
- **Debugging**: Shell-specific debugging and troubleshooting capabilities
- **Performance**: Shell optimization for healthcare application performance

### Environment Customization
- **Productivity Aliases**: Custom aliases for common healthcare compliance tasks
- **Prompt Customization**: Professional prompt display for development work
- **Environment Variables**: Healthcare-specific environment configuration
- **Path Management**: Efficient PATH configuration for development tools
- **History Management**: Command history optimization for efficiency

## Key Skills Demonstrated
- Advanced UNIX command-line operations
- Multiple argument and option usage
- Shell management and switching
- Environment customization and alias creation
- Professional command-line workflows
- System administration and automation

## Evidence of Completion
- Demonstration of cp, mkdir, less, mv, rm commands
- Multiple argument usage examples
- Shell identification and switching capabilities
- Alias creation and prompt customization
- Environment configuration documentation
- Advanced command-line workflow examples

## Technical Stack
- **Operating System**: Linux/UNIX (Ubuntu, CentOS, macOS Terminal)
- **Shells**: Bash, Zsh, Fish, Ksh, Csh
- **Commands**: Core UNIX utilities and advanced options
- **Text Editors**: vi/vim, nano, emacs for configuration
- **Configuration**: .bashrc, .zshrc, .profile files
- **Scripting**: Shell scripting for automation

## Advanced Commands Reference
```bash
# File Operations with Multiple Arguments
cp file1 file2 file3 /destination/          # Copy multiple files
cp -r source_dir1 source_dir2 /backup/      # Copy multiple directories
mkdir -p project/{backend,frontend,docs}    # Create nested directories
mkdir -m 755 dir1 dir2 dir3                 # Create directories with permissions

# File Movement and Removal
mv file1 file2 file3 /new_location/         # Move multiple files
mv old_dir new_dir                          # Rename directory
rm -rf dir1 dir2 dir3                       # Remove multiple directories
rm -i *.txt                                 # Interactive removal with pattern

# File Viewing with Options
less -N filename.txt                        # View with line numbers
less -S long_file.txt                       # View without line wrapping
less +G large_file.log                      # Start at end of file
less -p "search_term" file.txt              # Search for specific term

# Advanced Arguments and Options
ls -la /path/to/dir1 /path/to/dir2          # List multiple directories
find /path -name "*.txt" -exec rm {} \;     # Find and remove with arguments
grep -r "pattern" dir1 dir2 dir3            # Search multiple directories
chmod -R 755 dir1 dir2 dir3                 # Change permissions recursively
```

## Shell Management
```bash
# Shell Identification
echo $SHELL                                  # Display current shell
ps -p $$                                    # Show current shell process
cat /etc/shells                             # List available shells

# Shell Switching
bash                                        # Switch to Bash
zsh                                         # Switch to Zsh
fish                                        # Switch to Fish
exit                                        # Return to previous shell

# Shell-Specific Features
# Bash features
history | grep "command"                    # Command history search
!!                                          # Repeat last command
!$                                          # Last argument of previous command

# Zsh features
autoload -U compinit && compinit            # Enable completion
setopt AUTO_CD                              # Auto-change directory
setopt HIST_VERIFY                          # Verify history expansion
```

## Environment Customization
```bash
# Alias Creation
alias ll='ls -la'                           # List with details
alias la='ls -A'                            # List all files
alias l='ls -CF'                            # List in columns
alias ..='cd ..'                            # Go up one directory
alias ...='cd ../..'                        # Go up two directories
alias grep='grep --color=auto'              # Colorized grep
alias df='df -h'                            # Human-readable disk usage
alias du='du -h'                            # Human-readable directory size

# Healthcare-Specific Aliases
alias hipaa-check='python3 check_compliance.py'
alias backup-db='pg_dump hipaa_db > backup_$(date +%Y%m%d).sql'
alias start-services='systemctl start nginx postgresql redis'
alias view-logs='tail -f /var/log/hipaa-app.log'

# Prompt Customization
# Basic prompt
export PS1='\u@\h:\w$ '                     # user@host:directory$

# Advanced prompt with colors
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Healthcare project prompt
export PS1='\[\033[01;32m\]HIPAA@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Git-aware prompt (if using Git)
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;33m\]$(__git_ps1)\[\033[00m\]\$ '
```

## Configuration Files
```bash
# .bashrc Configuration
# Add to ~/.bashrc
export PATH="$PATH:/usr/local/bin"
export EDITOR="vim"
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoreboth

# Healthcare-specific environment variables
export HIPAA_DB_HOST="localhost"
export HIPAA_DB_PORT="5432"
export HIPAA_LOG_LEVEL="INFO"
export HIPAA_ENCRYPTION_KEY="your-encryption-key"

# Aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Functions
mkcd() { mkdir -p "$1" && cd "$1"; }
extract() {
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xjf $1     ;;
            *.tar.gz)    tar xzf $1     ;;
            *.bz2)       bunzip2 $1     ;;
            *.rar)       unrar e $1     ;;
            *.gz)        gunzip $1      ;;
            *.tar)       tar xf $1      ;;
            *.tbz2)      tar xjf $1     ;;
            *.tgz)       tar xzf $1     ;;
            *.zip)       unzip $1       ;;
            *.Z)         uncompress $1  ;;
            *.7z)        7z x $1        ;;
            *)           echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}
```

## Learning Outcomes
Upon completion of this course, students will be able to:
- Use advanced UNIX commands with multiple arguments and options
- Manage different shells and switch between them effectively
- Create and manage aliases for improved productivity
- Customize terminal environment and prompt display
- Build efficient command-line workflows
- Perform advanced system administration tasks

## Healthcare Compliance Integration
The UNIX implementation specifically addresses healthcare compliance needs:
- **Secure File Management**: Advanced file operations for sensitive healthcare data
- **Audit Logging**: Command-line logging for compliance tracking
- **Backup Management**: Advanced backup procedures for healthcare data
- **System Security**: Hardened shell configuration for HIPAA compliance
- **Access Control**: Role-based access control for healthcare systems

## Advanced File Operations
- **Batch Processing**: Multiple file operations for compliance data
- **Pattern Matching**: Advanced file selection and processing
- **Recursive Operations**: Directory tree operations for project management
- **Permission Management**: Advanced file permission handling
- **Archive Management**: File compression and archiving for backups

## Shell-Specific Features
- **Bash**: History expansion, brace expansion, command substitution
- **Zsh**: Advanced completion, globbing, and prompt themes
- **Fish**: User-friendly syntax and helpful features
- **Ksh**: POSIX compliance and advanced scripting
- **Csh**: C-like syntax and job control

## Productivity Enhancements
- **Alias Management**: Custom shortcuts for common tasks
- **Function Creation**: Reusable command sequences
- **Prompt Customization**: Informative and efficient prompt display
- **History Management**: Command history optimization
- **Tab Completion**: Enhanced command completion

---
*This course provides the advanced command-line foundation for the HIPAA Checklist Project, ensuring efficient system administration and secure file management for healthcare compliance applications.*
