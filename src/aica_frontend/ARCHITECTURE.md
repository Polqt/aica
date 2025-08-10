# Frontend Architecture Documentation

## Overview

This document describes the refactored frontend architecture following clean code principles: **SOLID**, **DRY**, **KISS**, **YAGNI**, and **Clean Code** practices.

## Architecture Principles Applied

### 1. Single Responsibility Principle (SRP)

- **Services**: Each service class has a single responsibility

  - `AuthService`: Only handles authentication operations
  - `ProfileService`: Only handles profile operations
  - `JobsService`: Only handles job-related operations
  - `HttpClient`: Only handles HTTP communication

- **Components**: Each component has a single responsibility
  - `RegisterForm`: Only handles user registration form
  - `LoginForm`: Only handles user login form

### 2. Open/Closed Principle (OCP)

- **Service Architecture**: Easy to extend with new services without modifying existing code
- **API Client**: Can be extended with new services through dependency injection

### 3. Liskov Substitution Principle (LSP)

- **HTTP Client**: Can be substituted with any client implementing the same interface
- **Services**: All services follow the same pattern and can be substituted

### 4. Interface Segregation Principle (ISP)

- **Type Definitions**: Specific interfaces for different concerns (API, Auth, Profile, etc.)
- **No fat interfaces**: Each interface serves a specific purpose

### 5. Dependency Inversion Principle (DIP)

- **Dependency Injection**: Services depend on abstractions, not concrete implementations
- **API Client Factory**: Injects dependencies into services

## Directory Structure

```
src/aica_frontend/
├── lib/
│   ├── services/           # Service layer (Business logic)
│   │   ├── api-client.ts   # Main API client factory
│   │   ├── auth.service.ts # Authentication service
│   │   ├── profile.service.ts # Profile service
│   │   ├── jobs.service.ts # Jobs service
│   │   ├── http-client.ts  # HTTP communication
│   │   └── index.ts        # Barrel exports
│   │
│   ├── utils/              # Utility functions
│   │   ├── token-manager.ts # Token storage management
│   │   ├── error-handler.ts # Error handling utilities
│   │   └── index.ts        # Barrel exports
│   │
│   ├── types/              # Type definitions
│   │   ├── api.ts          # API-related types
│   │   ├── profile.ts      # Profile types (existing)
│   │   └── jobs.ts         # Job types (existing)
│   │
│   ├── schemas/            # Validation schemas
│   │   └── validation.ts   # Centralized validation schemas
│   │
│   ├── hooks/              # Custom hooks
│   │   ├── useFormWithValidation.ts # Form handling hook
│   │   └── index.ts        # Barrel exports
│   │
│   └── context/            # React contexts
│       └── AuthContext.tsx # Authentication context
│
├── components/             # React components
│   ├── ui/                 # UI components (existing)
│   ├── RegisterForm.tsx    # Registration form
│   ├── LoginForm.tsx       # Login form
│   └── ...                 # Other components
│
└── app/                    # Next.js app directory
    └── ...                 # Pages and layouts
```

## Key Improvements Made

### 1. DRY (Don't Repeat Yourself)

- **Centralized Validation**: All validation schemas in one place
- **Reusable Hooks**: Form submission logic abstracted into reusable hooks
- **Common Error Handling**: Centralized error handling utilities
- **Shared Types**: Common API types to avoid duplication

### 2. KISS (Keep It Simple, Stupid)

- **Simple Service Layer**: Each service has a clear, simple responsibility
- **Clean API**: Easy-to-use API client with intuitive methods
- **Straightforward Components**: Components focus on presentation and user interaction

### 3. YAGNI (You Aren't Gonna Need It)

- **Minimal Abstractions**: Only necessary abstractions are implemented
- **Focused Features**: Only implemented what's currently needed
- **No Over-engineering**: Simple, effective solutions

### 4. Clean Code Practices

- **Meaningful Names**: Functions and variables have descriptive names
- **Small Functions**: Each function has a single responsibility
- **Clear Comments**: JSDoc comments explain the purpose of classes and methods
- **Consistent Formatting**: Consistent code style throughout

## Service Layer Architecture

### HTTP Client

```typescript
class HttpClient {
  // Handles all HTTP communication
  // Automatic retry logic
  // Error handling
  // Request/response transformation
}
```

### Authentication Service

```typescript
class AuthService {
  // Login/Register operations
  // Token management integration
  // Logout handling
}
```

### API Client Factory

```typescript
class ApiClient {
  // Dependency injection container
  // Service initialization
  // Centralized configuration
}
```

## Error Handling Strategy

### Centralized Error Handling

- **API Error Handler**: Parses and formats API errors consistently
- **HTTP Status Mapping**: Maps status codes to user-friendly messages
- **Type-safe Errors**: Proper TypeScript error types

### User Experience

- **Toast Notifications**: Immediate feedback for user actions
- **Inline Errors**: Form field validation errors
- **Loading States**: Clear indication of ongoing operations

## Type Safety

### Comprehensive Types

- **API Types**: Complete type definitions for API requests/responses
- **Form Types**: Type-safe form data structures
- **Service Types**: Strongly typed service interfaces

### Validation Integration

- **Zod Schemas**: Runtime validation with TypeScript integration
- **Form Validation**: Client-side validation with proper error handling

## Benefits Achieved

1. **Maintainability**: Clear separation of concerns makes code easier to maintain
2. **Testability**: Each service and component can be tested independently
3. **Reusability**: Common patterns abstracted into reusable utilities
4. **Type Safety**: Comprehensive TypeScript coverage prevents runtime errors
5. **Developer Experience**: Clear APIs and good documentation
6. **Performance**: Efficient error handling and loading states
7. **Scalability**: Easy to add new features without breaking existing code

## Usage Examples

### Using the API Client

```typescript
import { apiClient } from '@/lib/services';

// Login user
const response = await apiClient.auth.login({ email, password });

// Get profile
const profile = await apiClient.profile.getProfile();

// Get job recommendations
const jobs = await apiClient.jobs.getJobRecommendations();
```

### Using Form Hooks

```typescript
import { useFormSubmission } from '@/lib/hooks';

const { handleSubmit, isSubmitting, apiError } = useFormSubmission({
  onSubmit: async data => {
    await apiClient.auth.register(data);
  },
  successMessage: 'Registration successful!',
});
```

### Using Validation Schemas

```typescript
import { registerSchema } from '@/lib/schemas/validation';

const form = useForm({
  resolver: zodResolver(registerSchema),
  defaultValues: { email: '', password: '', confirmPassword: '' },
});
```

## Future Enhancements

1. **Caching Layer**: Add request caching for better performance
2. **Offline Support**: Implement offline functionality
3. **Real-time Updates**: Add WebSocket support for real-time features
4. **Advanced Error Recovery**: Implement automatic error recovery strategies
5. **Performance Monitoring**: Add performance tracking and monitoring
