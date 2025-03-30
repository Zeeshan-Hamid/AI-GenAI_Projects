import express from 'express';
import jwt from 'jsonwebtoken';
import { User } from '../models/User';
import { auth } from '../middleware/auth';
import { AuthRequest } from '../middleware/auth';

const router = express.Router();

// Signup route
router.post('/signup', async (req, res) => {
  try {
    const { email, password, name } = req.body;

    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ error: 'Email already registered' });
    }

    // Create new user
    const user = new User({ email, password, name });
    await user.save();

    // Generate token
    const token = jwt.sign({ _id: user._id }, process.env.JWT_SECRET!, {
      expiresIn: '7d'
    });

    res.status(201).json({ user, token });
  } catch (error) {
    res.status(400).json({ error: 'Error creating user' });
  }
});

// Login route
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find user
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Check password
    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate token
    const token = jwt.sign({ _id: user._id }, process.env.JWT_SECRET!, {
      expiresIn: '7d'
    });

    res.json({ user, token });
  } catch (error) {
    res.status(400).json({ error: 'Error logging in' });
  }
});

// Get current user
router.get('/me', auth, async (req: AuthRequest, res) => {
  res.json(req.user);
});

export default router; 