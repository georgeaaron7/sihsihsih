import { test, expect } from '@playwright/test';

test.describe('Argo Float Dashboard', () => {
  test('landing page loads and navigates to dashboard', async ({ page }) => {
    // Navigate to the landing page
    await page.goto('/');

    // Check that the landing page loaded
    await expect(page).toHaveTitle(/Argo Float Dashboard/);
    
    // Check for main heading
    await expect(page.locator('h1')).toContainText('Explore the');
    await expect(page.locator('h1')).toContainText('Deep Ocean');

    // Check for CTA button
    const ctaButton = page.locator('button', { hasText: 'Explore Dashboard' });
    await expect(ctaButton).toBeVisible();

    // Click the CTA button to navigate to dashboard
    await ctaButton.click();

    // Wait for navigation to dashboard
    await expect(page).toHaveURL('/dashboard');
    
    // Check dashboard loaded
    await expect(page.locator('h1')).toContainText('Float Dashboard');
  });

  test('dashboard loads float list and handles click', async ({ page }) => {
    // Navigate directly to dashboard
    await page.goto('/dashboard');

    // Wait for the page to load
    await expect(page.locator('h1')).toContainText('Float Dashboard');

    // Wait for float data to load (up to 10 seconds)
    await page.waitForSelector('[data-testid="float-card"], .loading-spinner', { timeout: 10000 });

    // Check if we have float cards or loading state
    const floatCards = page.locator('[data-testid="float-card"]');
    const loadingSpinner = page.locator('.loading-spinner');
    
    // Either we should see float cards or a loading spinner
    await expect(floatCards.first().or(loadingSpinner)).toBeVisible();

    // If float cards are present, test clicking on one
    const firstCard = floatCards.first();
    if (await firstCard.isVisible()) {
      const floatNumber = await firstCard.locator('h3').textContent();
      console.log('Clicking on float:', floatNumber);
      
      await firstCard.click();
      
      // Should navigate to float detail page
      await expect(page.url()).toMatch(/\/float\/\d+/);
      
      // Check that float detail page loaded
      await expect(page.locator('h1')).toContainText('Float');
    }
  });

  test('navigation works correctly', async ({ page }) => {
    await page.goto('/');

    // Test navigation menu
    const dashboardLink = page.locator('nav a[href="/dashboard"]');
    await expect(dashboardLink).toBeVisible();
    
    await dashboardLink.click();
    await expect(page).toHaveURL('/dashboard');

    // Test stats navigation
    const statsLink = page.locator('nav a[href="/stats"]');
    if (await statsLink.isVisible()) {
      await statsLink.click();
      await expect(page).toHaveURL('/stats');
      await expect(page.locator('h1')).toContainText('Statistics');
    }

    // Test home navigation
    const homeLink = page.locator('nav a[href="/"]');
    await homeLink.click();
    await expect(page).toHaveURL('/');
  });

  test('responsive design works on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('/');

    // Check that mobile navigation is present
    const mobileMenuButton = page.locator('button[aria-label="Toggle navigation menu"]');
    await expect(mobileMenuButton).toBeVisible();

    // Test mobile menu
    await mobileMenuButton.click();
    const mobileMenu = page.locator('nav').locator('div').last();
    await expect(mobileMenu).toBeVisible();

    // Navigate to dashboard from mobile menu
    await page.locator('nav a[href="/dashboard"]').click();
    await expect(page).toHaveURL('/dashboard');

    // Check that dashboard is responsive
    await expect(page.locator('h1')).toContainText('Float Dashboard');
  });

  test('error handling works correctly', async ({ page }) => {
    // Mock network failure
    await page.route('**/floats', route => route.abort());
    
    await page.goto('/dashboard');

    // Should show error state
    await expect(page.locator('text=Failed to Load Floats')).toBeVisible({ timeout: 10000 });
    
    // Should have retry button
    const retryButton = page.locator('button', { hasText: 'Try Again' });
    await expect(retryButton).toBeVisible();
  });
});

// Test accessibility
test.describe('Accessibility', () => {
  test('page has proper heading structure', async ({ page }) => {
    await page.goto('/');
    
    // Check for proper heading hierarchy
    const h1 = page.locator('h1');
    await expect(h1).toBeVisible();
    
    // Navigate to dashboard
    await page.locator('button', { hasText: 'Explore Dashboard' }).click();
    
    // Check dashboard headings
    await expect(page.locator('h1')).toContainText('Float Dashboard');
  });

  test('interactive elements are keyboard accessible', async ({ page }) => {
    await page.goto('/');
    
    // Test keyboard navigation
    await page.keyboard.press('Tab');
    
    // Should be able to focus on CTA button
    const ctaButton = page.locator('button', { hasText: 'Explore Dashboard' });
    await expect(ctaButton).toBeFocused();
    
    // Should be able to activate with Enter
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL('/dashboard');
  });
});
