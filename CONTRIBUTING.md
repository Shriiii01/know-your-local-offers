# 🤝 Contributing to Know Your Local Offers

Thank you for your interest in contributing to our AI-powered local business discovery platform! This document provides comprehensive guidelines and information for contributors.

## 🎯 How to Contribute

### 1Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/know-your-local-offers.git
cd know-your-local-offers
```

### 2. Set Up Development Environment
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes
- Follow the coding standards below
- Write tests for new features
- Update documentation as needed

### 5. Test Your Changes
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### 6. Commit and Push
```bash
git add .
git commit -m "feat: add new feature description"
git push origin feature/your-feature-name
```

### 7. Create a Pull Request
- Go to your fork on GitHub
- ClickNew Pull Request"
- Fill out the PR template
- Submit for review

## 📋 Pull Request Guidelines

### PR Title Format
```
type(scope): description

Examples:
feat(chat): add voice recognition support
fix(api): resolve CORS issue
docs(readme): update installation instructions
style(ui): improve button styling
refactor(backend): optimize database queries
test(api): add unit tests for offers endpoint
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- Bug fix
- ] New feature
- [ ] Breaking change
-cumentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
-  testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
-umentation updated
- [ ] Tests added/updated
```

## 🛠 Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names
- Add docstrings for functions and classes

```python
def get_user_offers(user_id: int, city: str) -> List[Offer]:
     Retrieve offers for a specific user in a given city.
    
    Args:
        user_id: The user's unique identifier
        city: The city to search for offers
        
    Returns:
        List of offers matching the criteria
        
    Raises:
        ValueError: If user_id is invalid
        DatabaseError: If database connection fails
    """
    # Implementation here
```

### TypeScript/JavaScript (Frontend)
- Use TypeScript for type safety
- Follow ESLint configuration
- Use functional components with hooks
- Implement proper error handling
- Use meaningful component and variable names

```typescript
interface OfferProps [object Object]
  offer: Offer;
  onSelect: (offer: Offer) => void;
}

const OfferCard: React.FC<OfferProps> = ({ offer, onSelect }) => {
  // Component implementation
};
```

### CSS/Styling
- Use Tailwind CSS utility classes
- Follow mobile-first responsive design
- Maintain consistent spacing and colors
- Use semantic class names

## 🧪 Testing Guidelines

### Backend Testing
- Write unit tests for all new functions
- Use pytest for testing framework
- Aim for >80de coverage
- Test both success and error cases

```python
def test_get_user_offers():
    st retrieving user offers."" offers = get_user_offers(user_id=1, city="Kolhapur")
    assert isinstance(offers, list)
    assert len(offers) >= 0
```

### Frontend Testing
- Write component tests using React Testing Library
- Test user interactions and state changes
- Mock API calls appropriately
- Test accessibility features

```typescript
test('renders offer card with correct data', () =>[object Object] render(<OfferCard offer={mockOffer} onSelect={jest.fn()} />);
  expect(screen.getByText(mockOffer.title)).toBeInTheDocument();
});
```

## 📚 Documentation Standards

### Code Documentation
- Add docstrings to all functions and classes
- Include parameter types and return values
- Provide usage examples for complex functions

### README Updates
- Update README.md for new features
- Include setup instructions for new dependencies
- Add screenshots for UI changes
- Update API documentation

### API Documentation
- Document all new endpoints
- Include request/response examples
- Specify authentication requirements
- List possible error codes

## 🐛 Bug Reports

### Before Submitting1ck existing issues for duplicates
2. Try to reproduce the bug
3s a configuration issue

### Bug Report Template
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS:e.g., macOS 120
- Browser: e.g., Chrome96
- Node.js: [e.g., 16.130]
- Python: [e.g., 3.120tional Information
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Before Submitting
1. Check if the feature already exists2sider if it aligns with project goals
3. Think about implementation complexity

### Feature Request Template
```markdown
## Feature Description
Clear description of the requested feature

## Use Case
Why this feature would be useful

## Proposed Implementation
How you think it could be implemented

## Alternatives Considered
Other approaches youve considered

## Additional Information
Any other relevant details
```

## 🏷 Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority: high`: High priority issues
- `priority: low`: Low priority issues
- `priority: medium`: Medium priority issues

## 🎉 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- GitHub contributors page

## 📞 Getting Help

If you need help with contributing:

1. **Check Documentation**: Read the README and existing docs
2**Search Issues**: Look for similar questions in existing issues3 **Create Issue**: Open a new issue with the `help wanted` label
4. **Join Discussions**: Participate in GitHub Discussions

## 🚀 Quick Start for New Contributors

1**Pick an Issue**: Look for issues labeled `good first issue`
2. **Set Up Environment**: Follow the setup instructions above3 **Make Changes**: Implement the feature or fix4ubmit PR**: Follow the PR guidelines5 **Get Feedback**: Respond to review comments

Thank you for contributing to Know Your Local Offers! 🎯