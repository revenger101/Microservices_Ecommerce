import { gql } from '@apollo/client';

// User Queries
export const GET_USERS = gql`
  query GetUsers {
    users {
      id
      username
      email
    }
  }
`;

export const CREATE_USER = gql`
  mutation CreateUser($username: String!, $email: String!, $password: String!) {
    createUser(username: $username, email: $email, password: $password) {
      success
      message
      user {
        id
        username
        email
      }
    }
  }
`;

// Order Queries
export const CREATE_ORDER = gql`
  mutation CreateOrder($userId: Int!, $items: [String!]) {
    createOrder(userId: $userId, items: $items) {
      success
      message
      order {
        id
        status
        items {
          product_id
          quantity
          price
        }
      }
    }
  }
`;

export const GET_ORDERS = gql`
  query GetOrders($userId: Int!) {
    orders(userId: $userId) {
      id
      status
      items {
        product_id
        quantity
        price
      }
    }
  }
`;
