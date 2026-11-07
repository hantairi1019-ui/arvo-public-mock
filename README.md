# ARVO Public Mock

ARVOのProject画面モックを公開・デモ閲覧するためのCanonical Mock Repositoryです。

## Repository Policy

- Visibility: **Public（意図された設定。Privateへ変更しない）**
- Canonical branch: `upstream`
- Canonical Mock: `<Project>/<Project>/mock/` ではなく、`<Project>/mock/`
- Projectの要件・Governance・Contract・Interface・Capability・Knowledgeの正本は `arvo-projects` に置く。
- モック本体は本Repositoryで作成・更新し、`arvo-projects` に重複配置しない。
- Project文書から該当するモックファイルへリンクする。

## Public Repository Safety

Public Repositoryであることを前提に、公開可能なモックと表示に必要な安全なアセットのみを配置する。

配置禁止:
- Secrets / Credentials / API Keys / Tokens
- 個人情報・顧客情報・機密情報
- 本番データ・実アカウント情報
- 非公開Project文書・内部運用情報
- 公開権限のない画像・フォント等のアセット

モックには架空のサンプルデータを使用し、公開前にソースとアセットを確認する。疑わしい情報が含まれる場合は公開せず、Humanに確認する。

## Project Mocks

| Project | Mock |
|---|---|
| P007 X運用管理SaaS | [P007 mock](P007-x-operations-management-saas/mock/index.html) |
