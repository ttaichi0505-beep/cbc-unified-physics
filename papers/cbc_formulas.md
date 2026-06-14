# CBC数式集

## 1. 状態の定義

\[
\mathcal{S} = \{1, i, -1, -i\} \quad \text{または} \quad \mathcal{S} = \{0°, 90°, 180°, 270°\}
\]

\[
\vec{v}(0°) = (1, 0), \quad \vec{v}(90°) = (0, 1), \quad \vec{v}(180°) = (-1, 0), \quad \vec{v}(270°) = (0, -1)
\]

## 2. 基本遷移ルール（万物の数式）

\[
\boxed{s(x, t+1) = \arg\max_{s' \in \mathcal{S}} \Re \left[ \left( \sum_{y \in \mathcal{N}(x)} s(y, t) \right) \cdot \overline{s'} \right]}
\]

## 3. 質量の定義

\[
r = \left\| \sum_i \vec{v}_i \right\| + \kappa \sum_{i,j} (1 - \vec{v}_i \cdot \vec{v}_j), \quad \kappa \approx 0.6
\]

## 4. 強い力（閉じ込め）

\[
\vec{V}_{\text{単独}} = \sum_{\text{近傍}} \vec{v}(s) \quad \Rightarrow \quad \text{不安定}
\]

\[
\vec{V}_{\text{三体}} = \sum_{k=1}^{3} \vec{v}(\text{クォーク}_k) \quad \Rightarrow \quad \text{安定}
\]

## 5. 弱い力（パリティ破れ）

\[
\text{バイアス} = \frac{N_{\text{左}} - N_{\text{右}}}{N_{\text{左}} + N_{\text{右}}} = 1.000
\]

## 6. 重力（状態密度の勾配）

\[
\vec{F}_{\text{重力}}(\vec{r}) = \gamma \nabla \rho(\vec{r}) \propto \frac{\partial \rho}{\partial x} \hat{i} + \frac{\partial \rho}{\partial y} \hat{j}
\]

## 7. 電磁気力（真空の歪みによる圧力差）

\[
F_x = \vec{v}(s_{\text{左}}) \cdot \vec{v}(s_{\text{自}}) - \vec{v}(s_{\text{右}}) \cdot \vec{v}(s_{\text{自}})
\]

## 8. 観測問題（ボルンの規則の導出）

\[
P(\text{一致}) = \frac{1 + \text{Sync}(A,B)}{2} = \cos^2\left(\frac{\Delta\theta}{2}\right)
\]

## 著者

Tai.ch (2026)
