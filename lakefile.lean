import Lake
open Lake DSL

package «deontic» where

lean_lib «Deontic» where
  roots := #[`Deontic]

lean_exe «deontic» where
  root := `Main
